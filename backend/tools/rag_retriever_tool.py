"""
RAG Retriever Tool - Memory System for Multi-Agent Framework
Uses ChromaDB for semantic search of relevant Bengali movie reviews
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from pydantic import BaseModel, Field

# Add paths
sys.path.append(str(Path(__file__).parent.parent / "config"))
from base_tool import BaseTool, ToolInput, ToolOutput
import config as cfg

# ChromaDB imports
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class RAGRetrieverInput(ToolInput):
    """Input schema for RAG Retriever"""
    query: str = Field(description="Movie plot or query text")
    persona: str = Field(description="Target persona: Die-hard Fan, Enthusiastic Casual, or Indifferent Casual")
    top_k: int = Field(default=5, description="Number of examples to retrieve")


class RAGRetrieverTool(BaseTool):
    """
    Retrieval-Augmented Generation Tool
    Searches CSV dataset for relevant review examples using semantic similarity
    """
    
    def __init__(self):
        super().__init__(name="RAGRetriever")
        
        # Initialize embedding model
        self.logger.info("Loading embedding model (LaBSE)...")
        self.embedding_model = SentenceTransformer('sentence-transformers/LaBSE')
        
        # Initialize ChromaDB with persistent storage
        self.logger.info("Initializing ChromaDB...")
        chroma_db_path = Path(__file__).parent.parent / "chroma_db"
        chroma_db_path.mkdir(exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path=str(chroma_db_path),
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Load and index data
        self._load_and_index_data()
        
        self.logger.info("RAG Retriever initialized successfully")
    
    def _extract_themes(self, plot: str) -> str:
        """Extract genre/theme keywords from plot for better matching"""
        plot_lower = plot.lower()
        themes = []
        
        # Genre detection (Bengali keywords)
        if any(word in plot_lower for word in ['রোমান্টিক', 'ভালোবাসা', 'প্রেম']):
            themes.append('রোমান্টিক ভালোবাসা')
        if any(word in plot_lower for word in ['রহস্য', 'থ্রিলার', 'গোয়েন্দা']):
            themes.append('রহস্য থ্রিলার')
        if any(word in plot_lower for word in ['স্বপ্ন', 'ভবিষ্যত', 'সতর্কবার্তা']):
            themes.append('স্বপ্ন ভবিষ্যত')
        if any(word in plot_lower for word in ['লড়াই', 'অপরাধী', 'সাহস']):
            themes.append('অ্যাকশন লড়াই')
        if any(word in plot_lower for word in ['পরিবার', 'সমাজ', 'বাধা']):
            themes.append('পারিবারিক ড্রামা')
        
        return ' '.join(themes) if themes else 'চলচ্চিত্র'
    
    def _load_and_index_data(self):
        """Load CSV data and create ChromaDB collection"""
        try:
            # Load CSV
            self.logger.info(f"Loading data from {cfg.CSV_FILE}")
            self.df = pd.read_csv(cfg.CSV_FILE)
            self.logger.info(f"Loaded {len(self.df)} reviews")
            
            # Map cluster to persona
            cluster_to_persona = {
                0: "Indifferent Casual",
                1: "Enthusiastic Casual", 
                2: "Die-hard Fan"
            }
            
            # Add persona column if not exists
            if 'persona' not in self.df.columns:
                cluster_col = 'cluster_label' if 'cluster_label' in self.df.columns else 'cluster'
                self.df['persona'] = self.df[cluster_col].map(cluster_to_persona)
                # Also create cluster column for metadata
                if 'cluster' not in self.df.columns:
                    self.df['cluster'] = self.df[cluster_col]
            
            # Try to get existing collection first
            try:
                self.collection = self.chroma_client.get_collection("bengali_reviews")
                self.logger.info("Using existing ChromaDB collection (already indexed)")
                return  # Skip indexing if collection exists
            except:
                self.logger.info("Creating new ChromaDB collection...")
                self.collection = self.chroma_client.create_collection(
                    name="bengali_reviews",
                    metadata={"description": "Bengali movie reviews with personas"}
                )
                
                # Index all reviews
                self.logger.info("Indexing reviews (this may take a few minutes)...")
                batch_size = 100
                for i in range(0, len(self.df), batch_size):
                    batch = self.df.iloc[i:i+batch_size]
                    
                    # Prepare data
                    documents = batch['review'].tolist()
                    ids = [f"review_{idx}" for idx in batch.index]
                    metadatas = [
                        {
                            "persona": row['persona'],
                            "cluster": int(row['cluster']),
                            "sentiment": float(row.get('sentiment', 3.0))
                        }
                        for _, row in batch.iterrows()
                    ]
                    
                    # Generate embeddings
                    embeddings = self.embedding_model.encode(
                        documents, 
                        convert_to_numpy=True,
                        show_progress_bar=False
                    ).tolist()
                    
                    # Add to collection
                    self.collection.add(
                        documents=documents,
                        embeddings=embeddings,
                        metadatas=metadatas,
                        ids=ids
                    )
                    
                    if (i + batch_size) % 500 == 0:
                        self.logger.info(f"Indexed {i + batch_size}/{len(self.df)} reviews")
                
                self.logger.info("Indexing complete!")
        
        except Exception as e:
            self.logger.error(f"Failed to load data: {e}")
            raise
    
    def _execute(self, input_data: RAGRetrieverInput) -> ToolOutput:
        """
        Retrieve relevant review examples based on query and persona
        """
        try:
            # Preprocess query for better matching
            # Extract key themes from plot for semantic search
            query_text = input_data.query
            
            # Add genre/theme keywords to improve matching
            # This helps match plot themes with review sentiments
            theme_keywords = self._extract_themes(query_text)
            enhanced_query = f"{query_text} {theme_keywords}"
            
            self.logger.info(f"Original query: {query_text[:100]}...")
            self.logger.info(f"Enhanced query: {enhanced_query[:100]}...")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(
                [enhanced_query],
                convert_to_numpy=True,
                show_progress_bar=False
            ).tolist()[0]
            
            # Search with persona filter
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=input_data.top_k * 2,  # Get more to filter by persona
                where={"persona": input_data.persona}
            )
            
            # Format results
            examples = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    if i >= input_data.top_k:
                        break
                    
                    # ChromaDB uses L2 distance - lower is better
                    # Convert to similarity score (0-1, higher is better)
                    similarity = max(0, 1 - (distance / 2))  # Normalize L2 distance
                    
                    examples.append({
                        "review": doc,
                        "persona": metadata['persona'],
                        "sentiment": metadata.get('sentiment', 3.0),
                        "similarity": similarity,
                        "distance": distance  # Keep for debugging
                    })
            
            # Create context for LLM
            context = self._format_context(examples, input_data.persona)
            
            return ToolOutput(
                success=True,
                data={
                    "examples": examples,
                    "context": context,
                    "count": len(examples)
                },
                metadata={
                    "query": input_data.query,
                    "persona": input_data.persona,
                    "top_k": input_data.top_k
                }
            )
        
        except Exception as e:
            self.logger.error(f"Retrieval failed: {e}")
            return ToolOutput(
                success=False,
                data=None,
                error=str(e)
            )
    
    def _format_context(self, examples: List[Dict], persona: str) -> str:
        """Format examples as context for LLM"""
        if not examples:
            return f"No examples found for {persona}."
        
        context = f"REFERENCE EXAMPLES (for STYLE ONLY - DO NOT copy content):\n"
        context += f"These are {len(examples)} example reviews from '{persona}' persona.\n"
        context += f"Learn the WRITING STYLE, TONE, and LANGUAGE from these examples.\n"
        context += f"DO NOT copy plot details from examples. Write about YOUR movie plot.\n\n"
        
        for i, ex in enumerate(examples[:5], 1):  # Limit to 5 for clarity
            context += f"Example {i} (Style Reference - Similarity: {ex['similarity']:.2f}):\n"
            context += f"{ex['review'][:200]}...\n\n"  # Truncate to avoid copying
        
        context += f"\nNow write YOUR review about YOUR movie plot in the style of '{persona}' persona.\n"
        context += f"Focus on YOUR movie's plot, characters, and story - NOT the examples above."
        
        return context


# Test the tool
if __name__ == "__main__":
    print("=" * 60)
    print("Testing RAG Retriever Tool")
    print("=" * 60)
    
    # Initialize tool
    print("\nInitializing RAG Retriever...")
    tool = RAGRetrieverTool()
    
    # Test query
    test_input = RAGRetrieverInput(
        query="একটি রোমান্টিক মুভি যেখানে প্রেমিক-প্রেমিকা আলাদা হয়ে যায়",
        persona="Die-hard Fan",
        top_k=3
    )
    
    print(f"\nQuery: {test_input.query}")
    print(f"Persona: {test_input.persona}")
    print(f"Top K: {test_input.top_k}")
    
    # Run retrieval
    print("\nRetrieving examples...")
    output = tool.run(test_input)
    
    # Display results
    if output.success:
        print(f"\n[SUCCESS] Retrieved {output.data['count']} examples")
        print("\nExamples:")
        for i, ex in enumerate(output.data['examples'], 1):
            print(f"\n{i}. Similarity: {ex['similarity']:.3f}")
            print(f"   Review: {ex['review'][:100]}...")
        
        print("\n" + "=" * 60)
        print("Context for LLM:")
        print("=" * 60)
        print(output.data['context'][:500] + "...")
    else:
        print(f"\n[FAILED] {output.error}")
    
    print("\n" + "=" * 60)
    print("RAG Retriever Test Complete")
    print("=" * 60)

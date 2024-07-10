"""
Serializers for embedding APIs.
"""
from rest_framework import serializers
from app_core.models import LangchainPgEmbedding
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import PGVector
from langchain_nomic.embeddings import NomicEmbeddings


class EmbeddingSerializer(serializers.ModelSerializer):
    """Serializer for Embeddings."""

    url = serializers.URLField(write_only=True)

    class Meta:
        model = LangchainPgEmbedding
        fields = ['uuid', 'url', 'document']
        read_only_fields = ['uuid', 'document']

    def create(self, validated_data):
        """Create embeddings from a URL."""
        url = validated_data['url']

        # Fetch the content from the URL
        docs = WebBaseLoader(url).load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        doc_splits = text_splitter.split_documents(docs)

        # Add to vectorDB
        PGVector.from_documents(
            documents=doc_splits,
            collection_name="rag-pgvector",
            embedding=NomicEmbeddings(
                model="nomic-embed-text-v1.5", inference_mode="local"),
            use_jsonb=True
        )

        return url

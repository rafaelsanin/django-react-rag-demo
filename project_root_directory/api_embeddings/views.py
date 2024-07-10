from rest_framework import viewsets, authentication
from rest_framework.permissions import IsAuthenticated
from app_core.models import LangchainPgEmbedding
from api_embeddings.serializers import EmbeddingSerializer


class EmbeddingViewSet(viewsets.ModelViewSet):
    """Manage embeddings in the database"""
    serializer_class = EmbeddingSerializer
    queryset = LangchainPgEmbedding.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Perform the creation of an embedding."""
        serializer.save(user=self.request.user)

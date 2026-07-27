from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsCertificateOwner
from .selectors import get_certificate_by_number, get_user_certificates
from .serializers import CertificateSerializer


class CertificateListView(ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return get_user_certificates(user)
    

class CertificateDetailView(RetrieveAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated, IsCertificateOwner]

    def get_object(self):
        pk = self.kwargs.get('pk')
        certificates = get_user_certificates(self.request.user)

        if hasattr(certificates, 'filter'):
            obj = certificates.filter(pk=pk).first()
        else:
            obj = next((c for c in certificates if str(c.id) == str(pk)), None)

        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound()

        self.check_object_permissions(self.request, obj)
        return obj

class CertificateValidationView(APIView):
    """
    Public — for external verification of the certificate via QR code.
    """
    permission_classes = [AllowAny]

    def get(self, request, certificate_number):
        certificate = get_certificate_by_number(certificate_number)
        if not certificate:
            return Response({"valid": False}, status=404)
        return Response({"valid": True, "data": CertificateSerializer(certificate).data})
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_otp.plugins.otp_totp.models import TOTPDevice

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_mfa(request):
    user = request.user
    device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
    # Use qrcode generation or return config URL
    if created:
        return Response({"message": "MFA device created.", "config_url": device.config_url})
    return Response({"message": "MFA already enabled."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_mfa(request):
    user = request.user
    token = request.data.get("otp_token")
    if not token:
        return Response({"error": "No OTP provided."}, status=400)
        
    device = TOTPDevice.objects.filter(user=user, name='default').first()
    if device and device.verify_token(token):
        return Response({"message": "MFA verified successfully."})
    
    return Response({"error": "Invalid OTP."}, status=401)

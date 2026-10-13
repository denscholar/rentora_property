import requests

from django.conf import settings

from accounts.utils.phone_numbers import normalize_phone_number


class TermiiService:

    @staticmethod
    def send_sms(
        *,
        phone_number: str,
        otp: str,
    ) -> dict:
        """
        Send an SMS through Termii.

        Uses the DND channel for transactional messages,
        such as tenant phone verification OTPs.
        """

        if not phone_number:
            raise ValueError("Phone number is required.")

        if not otp:
            raise ValueError("SMS message is required.")

        if not settings.TERMII_API_KEY:
            raise ValueError(
                "TERMII_API_KEY has not been configured."
            )

        # Normalize the number to E.164.
        # Example: +2348012345678
        normalized_phone = normalize_phone_number(
            phone_number,
            default_region="NG",
        )

        # Termii expects the international number without "+".
        # Example: 2348012345678
        termii_phone_number = normalized_phone.removeprefix("+")

        base_url = settings.TERMII_BASE_URL.rstrip("/")
        url = f"{base_url}/api/sms/send"

        payload = {
            "api_key": settings.TERMII_API_KEY,
            "to": termii_phone_number,
            "from": settings.TERMII_SENDER_ID,
            "sms": otp,
            "type": "plain",
            "channel": "dnd",
        }

        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=15,
            )
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(
                "Termii SMS request failed."
            ) from exc

        try:
            response_data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Termii returned an invalid response."
            ) from exc

        if not response.ok:
            raise RuntimeError(
                f"Termii SMS failed (HTTP {response.status_code}): "
                f"{response_data}"
            )

        return response_data
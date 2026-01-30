import logging

from django.core.cache import cache

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from config.data_gouv_api import DataGouvAPI
from config.matomo_api import MatomoAPI

logger = logging.getLogger(__name__)


class StatsRequestError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class StatsView(APIView):
    """
    Cet endpoint expose les statistiques hors Metabase (par example, Matomo)
    """

    def get(self, request, format=None):
        # Dans un premier temps on vérifie dans le cache.
        cache_key = "stats_cache"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Serving cached data for {cache_key}")
            return Response(cached_data)

        data = {
            "element_visit_stats": MatomoAPI().get_page_evolution(),
            "declaration_visit_stats": DataGouvAPI().get_declaration_stats(),
            "csp_nonce": str(getattr(request, "_csp_nonce", "")),
        }

        # Cache pour une heure
        cache.set(cache_key, data, timeout=3600)
        return Response(data)

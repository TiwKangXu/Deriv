class RoutingService:
    @staticmethod
    def get_route(
        category: str,
        routing_rules: dict
    ) -> str:
        return routing_rules.get(
            category,
            "manual_review_queue"
        )
from collections import Counter


class SummaryService:

    @staticmethod
    def build_summary(
        final_queue: list,
        overrides: list
    ) -> str:

        total_count = len(final_queue)

        category_counter = Counter(
            item["final_category"]
            for item in final_queue
        )

        priority_counter = Counter(
            item["final_priority"]
            for item in final_queue
        )

        route_counter = Counter(
            item["final_route_to"]
            for item in final_queue
        )

        lines = []

        lines.append("# Queue Summary\n")

        lines.append(
            f"## Total Ticket Count\n\n"
            f"{total_count}\n"
        )

        lines.append(
            "## Count By Final Category\n"
        )

        for key, value in category_counter.items():
            lines.append(
                f"- {key}: {value}"
            )

        lines.append("")

        lines.append(
            "## Count By Final Priority\n"
        )

        for key, value in priority_counter.items():
            lines.append(
                f"- {key}: {value}"
            )

        lines.append("")

        lines.append(
            "## Queue Breakdown By Destination\n"
        )

        for key, value in route_counter.items():
            lines.append(
                f"- {key}: {value}"
            )

        lines.append("")

        lines.append(
            "## Overridden Tickets\n"
        )

        if not overrides:

            lines.append(
                "No overrides applied."
            )

        else:

            for override in overrides:

                lines.append(
                    f"- {override['ticket_id']}: "
                    f"{override['old_category']}"
                    f" -> "
                    f"{override['new_category']} | "
                    f"{override['old_priority']}"
                    f" -> "
                    f"{override['new_priority']}"
                )

        lines.append("")

        return "\n".join(lines)
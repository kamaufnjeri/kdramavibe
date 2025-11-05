# admin.py
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from .models import DramabeansKdrama, Kdrama, DramabeansKactor, Kactor
from kdramavibe_scrapper.utils import CompareKdramas, CompareKactors
from django.core.paginator import Paginator


@admin.register(DramabeansKdrama)
class DramabeansKdramaAdmin(admin.ModelAdmin):
    """
    Admin class for DramabeansKdrama with custom compare and link views.
    """
    list_display = ("title", "linked_to", "year")
    actions = ["unlink_selected"]
    change_list_template = "admin/kdrama_compare_list.html"  # Custom template

    def linked_to(self, obj):
        """Display linked Kdrama title or ❌ None if not linked."""
        return obj.kdrama.title if obj.kdrama else "❌ None"
    linked_to.short_description = "Linked Kdrama"

    def get_urls(self):
        """
        Add custom URLs for comparison and linking actions.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "compare/",
                self.admin_site.admin_view(self.compare_view),
                name="compare-kdramas",
            ),
            path(
                "link/",
                self.admin_site.admin_view(self.link_selected),
                name="link-kdramas",
            ),
        ]
        return custom_urls + urls

    def compare_view(self, request):
        """
        Display paginated DramabeansKdramas with best-matching Kdramas.

        Filters only unlinked DramabeansKdramas and Kdramas.
        """
        threshold = int(request.GET.get("threshold", 80))
        page_number = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 40))

        # Fetch unlinked DramabeansKdramas
        dramabeans_qs = DramabeansKdrama.objects.filter(
            kdrama__isnull=True
        ).order_by("title")

        # Paginate the queryset
        paginator = Paginator(dramabeans_qs, page_size)
        page = paginator.get_page(page_number)

        matches = []

        # Compare only the current page items
        unlinked_kdramas = Kdrama.objects.filter(dramabeans_details__isnull=True)

        for d in page.object_list:
            best_match = None
            best_score = 0

            for k in unlinked_kdramas:
                cmp = CompareKdramas(d, k, threshold)
                result = cmp.match_details()

                # Update best match if score is higher
                if result["best_score"] > best_score:
                    best_match = result
                    best_score = result["best_score"]

            if best_match and best_match["is_match"]:
                matches.append(best_match)

        context = {
            "page_obj": page,
            "matches": matches,
            "paginator": paginator,
            "is_paginated": paginator.num_pages > 1,
            "opts": self.model._meta,
            "threshold": threshold,
        }

        return render(request, "admin/kdrama_compare_results.html", context)

    def link_selected(self, request):
        """
        Handle POST request to link selected DramabeansKdramas to Kdramas.
        """
        selected_ids = request.POST.getlist("selected")
        linked_count = 0

        for pair_id in selected_ids:
            d_id, k_id = pair_id.split("__")
            d = DramabeansKdrama.objects.get(id=d_id)
            k = Kdrama.objects.get(id=k_id)
            d.kdrama = k
            d.save()
            linked_count += 1

        self.message_user(
            request, f"{linked_count} Kdramas linked successfully.", messages.SUCCESS
        )
        # Redirect back to comparison page
        return redirect(f"{request.path.replace('link/', 'compare/?page=1')}")

    @admin.action(description="Unlink selected DramabeansKdramas")
    def unlink_selected(self, request, queryset):
        """Unlink selected DramabeansKdramas."""
        count = queryset.update(kdrama=None)
        self.message_user(request, f"{count} Kdramas unlinked.", messages.INFO)


@admin.register(DramabeansKactor)
class DramabeansKactorAdmin(admin.ModelAdmin):
    """
    Admin class for DramabeansKactor with custom compare and link views.
    """
    list_display = ("name", "linked_to")
    actions = ["unlink_selected"]
    change_list_template = "admin/kactor_compare_list.html"  # Custom template

    def linked_to(self, obj):
        """Display linked Kactor name or ❌ None if not linked."""
        return obj.kactor.name if obj.kactor else "❌ None"
    linked_to.short_description = "Linked Kactor"

    def get_urls(self):
        """
        Add custom URLs for comparison and linking actions.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "compare/",
                self.admin_site.admin_view(self.compare_view),
                name="compare-kactors",
            ),
            path(
                "link/",
                self.admin_site.admin_view(self.link_selected),
                name="link-kactors",
            ),
        ]
        return custom_urls + urls

    def compare_view(self, request):
        """
        Display paginated DramabeansKactors with best-matching Kactors.

        Filters only unlinked DramabeansKactors and Kactors.
        """
        threshold = int(request.GET.get("threshold", 50))
        page_number = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 50))

        # Fetch unlinked DramabeansKactors
        dramabeans_qs = DramabeansKactor.objects.filter(
            kactor__isnull=True
        ).order_by("name")

        # Paginate the queryset
        paginator = Paginator(dramabeans_qs, page_size)
        page = paginator.get_page(page_number)

        matches = []

        # Compare only current page items
        unlinked_kactors = Kactor.objects.filter(dramabeans_details__isnull=True)

        for d in page.object_list:
            best_match = None
            best_score = 0

            for k in unlinked_kactors:
                cmp = CompareKactors(d, k, threshold)
                result = cmp.match_details()

                # Update best match if score is higher
                if result["best_score"] > best_score:
                    best_match = result
                    best_score = result["best_score"]

            if best_match and best_match["is_match"]:
                matches.append(best_match)

        context = {
            "page_obj": page,
            "matches": matches,
            "paginator": paginator,
            "is_paginated": paginator.num_pages > 1,
            "opts": self.model._meta,
            "threshold": threshold,
        }

        return render(request, "admin/kactor_compare_results.html", context)

    def link_selected(self, request):
        """
        Handle POST request to link selected DramabeansKactors to Kactors.
        """
        selected_ids = request.POST.getlist("selected")
        linked_count = 0

        for pair_id in selected_ids:
            d_id, k_id = pair_id.split("__")
            d = DramabeansKactor.objects.get(id=d_id)
            k = Kactor.objects.get(id=k_id)
            d.kactor = k
            d.save()
            linked_count += 1

        self.message_user(
            request, f"{linked_count} Kactor linked successfully.", messages.SUCCESS
        )
        # Redirect back to comparison page
        return redirect(f"{request.path.replace('link/', 'compare/?page=1')}")

    @admin.action(description="Unlink selected DramabeansKactors")
    def unlink_selected(self, request, queryset):
        """Unlink selected DramabeansKactors."""
        count = queryset.update(kactor=None)
        self.message_user(request, f"{count} Kactors unlinked.", messages.INFO)

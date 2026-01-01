from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from .models import Order, OrderItem


class TodayOrderFilter(admin.SimpleListFilter):
    title = "Order date"
    parameter_name = "order_date"

    def lookups(self, request, model_admin):
        return (
            ("today", "Today"),
            ("last_7_days", "Last 7 days"),
            ("this_month", "This month"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()

        if self.value() == "today":
            return queryset.filter(created_at__date=now.date())

        if self.value() == "last_7_days":
            return queryset.filter(created_at__gte=now - timedelta(days=7))

        if self.value() == "this_month":
            return queryset.filter(
                created_at__year=now.year,
                created_at__month=now.month,
            )

        return queryset


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "size_ml", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 🔥 DEFAULT ORDER
    ordering = ("-created_at",)

    # 👀 LIST VIEW
    list_display = (
        "id",
        "user",
        "total_amount",
        "colored_status",
        "payment_status",
        "created_at",
    )

    # 🎛 FILTERS
    list_filter = (
        "status",
        "payment_status",
        TodayOrderFilter,
    )

    # 🔍 SEARCH
    search_fields = (
        "id",
        "user__email",
        "phone",
        "full_name",
    )

    # 📦 INLINE ITEMS
    inlines = [OrderItemInline]

    # 🧠 READONLY
    readonly_fields = (
        "user",
        "total_amount",
        "created_at",
    )

    # 🎨 STATUS BADGES
    def colored_status(self, obj):
        colors = {
            "pending": "#d97706",   # amber
            "paid": "#059669",      # green
            "shipped": "#2563eb",   # blue
        }
        color = colors.get(obj.status, "#000")

        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            color,
            obj.status.upper()
        )

    colored_status.short_description = "Status"

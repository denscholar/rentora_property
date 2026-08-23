from accounts.models import CustomUser


ADMIN_PERMISSIONS = {
    CustomUser.AdminType.SUPER_ADMIN: {
        "property_moderation.view",
        "property_moderation.approve",
        "property_moderation.reject",
        "property_moderation.request_information",
        "property_moderation.unpublish",

        # Future permissions can be added here.
        # "users.manage",
        # "payments.manage",
        # "settings.manage",
    },

    CustomUser.AdminType.PROPERTY_MODERATOR: {
        "property_moderation.view",
        "property_moderation.approve",
        "property_moderation.reject",
        "property_moderation.request_information",
        "property_moderation.unpublish",
    },

    CustomUser.AdminType.FINANCE_ADMIN: {
        "finance.view",
        "finance.manage",
    },

    CustomUser.AdminType.SUPPORT_ADMIN: {
        "support.view",
        "support.manage",
    },

    CustomUser.AdminType.OPERATIONS_ADMIN: {
        "property_moderation.view",
        "property_moderation.unpublish",
    },
}
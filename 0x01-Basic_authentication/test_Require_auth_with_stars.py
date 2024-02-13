from api.v1.auth.auth import Auth
auth_instance = Auth()
excluded_paths = ["/api/v1/stat*"]

print(auth_instance.require_auth("/api/v1/users", excluded_paths))
print(auth_instance.require_auth(
    "/api/v1/status", excluded_paths))
print(auth_instance.require_auth("/api/v1/stats", excluded_paths))

from app.services.map_service import get_route_summary

route = get_route_summary(
    origin_name="深圳大学",
    origin_location="113.9304,22.5333",
    destination_name="深圳湾公园",
    destination_location="113.9499,22.5072",
    city="深圳",
)

print(route.model_dump())
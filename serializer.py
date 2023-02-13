from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer

serializer = URLSafeTimedSerializer("cisco12345")
non_timed_serializer = URLSafeSerializer("cisco12345")

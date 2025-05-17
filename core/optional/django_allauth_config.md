
# Django Allauth Konfiguration für Discord

## Installierte Apps
```python
INSTALLED_APPS += [
  "allauth",
  "allauth.account",
  "allauth.socialaccount",
  "allauth.socialaccount.providers.discord",
]
```

## OAuth2-Konfiguration
```python
SOCIALACCOUNT_PROVIDERS = {
  'discord': {
    'SCOPE': ['identify', 'email', 'guilds'],
  }
}
```

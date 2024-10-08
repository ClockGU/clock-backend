

# Workflow für supervisor app

## AuthKey Model

Dieses Model existiert um sicherzustellen, dass nur ausgewählte Personen
zugang zum `Supervisor-Frontend` bekommen.

1. Die Erstellung einer AuthKey Instanz benötigt lediglich eine Email-Adresse.
2. Bei der Erstellung des Datenbankeintrags wird ein RSA Key mit `key_size=1024` erstellt und gespeichert.
3. Anschließend wird eine Mail an die gespeicherte Email-Adresse mit einem Auth-Token gesendet.
4. Der Auth-Token ist eine encryptete Dictionary des erstellten RSA Key und der Email-Adresse:

```
...
encrypt(
  bytes(
    json.dumps({key: <key>, email: <email>}),
    "utf-8"
  )
)
```


## API /supervisor/verify

POST payload
```
 {
   auth_key: <String>
 }
```

1. Versuche `auth_key` zu `decrypt`'en und mit `json.loads(result)` einen Dictonary daraus zu erhalten.
   1. InvalidToken: Nutzer hat einen `auth_key` geschickt der nicht vom System erstellt wurde.
   Return HTTP 400 error: "Invalid Key: Key was not generated by the System."
   2. JSONDecodeError: Return HTTP 400 error: "Invalid key: Decrypted data is not JSON serializable."
2. Versuche aus JSON decoded Objekt `key` und `email` zu extrahieren
   1. KeyError: Return HTTP 400 error "Invalid Data: Encrypted data does not contain necessary "
3. Versuche AuthKey mit `key=<key>` zu finden
   1. ObjectDoesNotExist: Return HTTP 400 error: "Invalid Data: The provided key can no longer be used for authentication."
4. Überprüfe ob die `email` der AuthKey Instanz mit der der `request.user` und mit der des JSON Objektes übereinstimmt.
   1. False: Return HTTP 401 error: "Unauthorized"
5. Setze `is_supervisor=True` für ausgewählten Nutzer
6. Lösche Authkey
7. 200 OK


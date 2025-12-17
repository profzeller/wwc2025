# NETLAB+ Access

- URL: [https://labs.fhsu.edu](https://labs.fhsu.edu)
- Username: (email address you registered with)
- Password: `wwc2025!` (change on first login)

---

1. Launch the lab environment.
2. Inside client1, click on the Docker Desktop icon on the left (whale).
3. Once up you can minimize, not close that window.
4. Click on the Terminal icon on the left above the whale.
5. Use the following command to get into the labs folder:

```bash
cd wwc2025-labs
```

6. Then update the git repo:

```bash
git pull
```

7. Rebuild labs:

```bash
docker compose --profile labs build
```

8. Start the hub:

```bash
docker compose up -d hub
```

9. Launch Firefox and go to the following URL:

http://localhost:8080
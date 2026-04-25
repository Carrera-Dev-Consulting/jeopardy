db.createUser(
    {
        user: "test_user",
        pwd: "admin",
        roles: [
            {
                role: "readWrite",
                db: "zombie_nomnom"
            }
        ]
    }
);
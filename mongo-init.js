db = db.getSiblingDB('rankings');

db.createCollection('club_info');

db.club_info.insertMany([
    {
        names: ["redolat team", "redolatteam", " redolat"],
    },
]);
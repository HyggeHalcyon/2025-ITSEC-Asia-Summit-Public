const express = require('express');
const sqlite3 = require('sqlite3');
const { v4: uuidv4 } = require('uuid');
const cors = require('cors');

const app = express();
const PORT = 5599;
const db = new sqlite3.Database("planner.db");
const unnecessaryChar = "abbr acronym address applet area article aside audio base bdi bdo big blink blockquote br button canvas caption center cite code col colgroup command content data datalist dd del details dfn dialog dir div dl dt element em embed fieldset figcaption figure font footer form frame frameset head header hgroup hr html iframe image input kbd keygen label legend li link listing location main map mark marquee menu menuitem meta meter multicol nav nextid nobr noembed noframes noscript object optgroup output param picture plaintext pre progress samp script section select shadow slot small source spacer span strike strong sub . summary sup svg table tbody td template textarea tfoot th thead time tr track tt ul var video replace eval ( ) `".split(" ")

function Migrate(){
    db.exec(`
        DROP TABLE IF EXISTS Plans;
        CREATE TABLE Plans(
            uuid CHAR(36) PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            important_type INTEGER NOT NULL
        );
        `);
}

Migrate();

const CreatePlan = db.prepare("INSERT INTO Plans (uuid, title, description, important_type) VALUES (?, ?, ?, ?)");
app.use(cors());
app.use(express.json());

app.get("/", (req,res) => {
    res.send("Connection OK");
});

app.get("/get-plan/:uuid", (req, res) => {
    const uuid = req.params.uuid;
    db.get("SELECT * FROM Plans WHERE uuid = ?", [uuid], (err, row) => {
        if (err) return res.status(500).json({ message:"error", error: err.message });
        if (!row) return res.status(404).json({ message: "plan not found" });
        res.status(200).json({ message: "success", plan: row });
    });
});

app.post("/create-plan", (req, res) => {
    let { title, description, important_type } = req.body;
    if (!title || !description || important_type === undefined) {
        return res.status(400).json({ message: "A field is missing" });
    }

    if (typeof important_type !== 'number') {
        return res.status(400).json({ message: "important_type should be a number" });
    }

    if (important_type < 1 || important_type > 3) {
        return res.status(400).json({ message: "important_type should be ranged 1-3" });
    }
    const escapeRegExp = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    for (const c of unnecessaryChar) {
        const pattern = new RegExp(escapeRegExp(c), 'gi');
        description = description.replace(pattern, '');
    }

    const uuid = uuidv4();

    try {
        CreatePlan.run(uuid, title, description, important_type);
        return res.status(201).json({ message: "success", plan: uuid });
    } catch (e) {
        return res.status(500).json({ message: "error creating plan", error: e.message });
    }
});

app.listen(PORT, async () => {
    console.log(`App Started in http://localhost:${PORT}`);
});
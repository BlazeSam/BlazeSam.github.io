require("dotenv").config();
const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.post("/send-email", async (req, res) => {
    const { email, response } = req.body;

    if (!email || !response) {
        return res.status(400).json({ error: "Email and response are required!" });
    }

    try {
        const resendResponse = await fetch("https://api.resend.com/emails", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${process.env.RESEND_API_KEY}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                from: "onboarding@resend.dev",  // use this for testing
                to: email,
                subject: "Your Response 💌",
                text: `You clicked: ${response}`
            })
        });

        const data = await resendResponse.json();

        if (!resendResponse.ok) {
            return res.status(500).json({ error: data });
        }

        res.json({ success: true, data });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Failed to send email." });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

import express from "express"
import cors from "cors"
import mongoose from "mongoose"
import Exercise from "./models/exercise.js"
import userRouter from "./routes/userRoute.js"
import "dotenv/config"



//app config
const app = express()
const port = 4000

//middlewares
app.use(express.json())
app.use(cors())

main()
    .then(()=>{
        console.log("connceted to db");
    })
    .catch((err)=>{
        console.log(err);
    });

//Database
async function main() {
    await mongoose.connect('mongodb://127.0.0.1:27017/AI-fitness-trainer');
}


//api end points
app.get('/',(req,res)=>{
    res.send('API WORKING');
})


app.use("/api/user",userRouter)

app.get("/testExercise",async (req,res)=>{
    let sampleExercise = new Exercise({
         
            name: "Bicep Curls",
            image: 'bicep',
            description: "Isolates and strengthens the biceps, enhancing upper arm definition.",
            category: "Arms"
    });

    await sampleExercise.save();
    console.log("sample was saved");
    res.send("sample saved");
    
})

app.listen(port,()=>{
    console.log(`Server started on http://localhost:${port}`);
    
})
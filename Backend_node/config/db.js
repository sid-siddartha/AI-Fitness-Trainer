import mongoose from 'mongoose';

const MONGO_URL = 'mongodb://127.0.0.1:27017/Ai-fitness-trainer';
main().then(()=>{
    console.log('connection successfull');
    })
.catch((err)=>{
    console.log(err);
    
})

async function main(){
    await mongoose.connect(MONGO_URL)
}


const initDB = async()=>{
    await Listing.deleteMany({});
    initData.data = initData.data.map((obj)=>({
        ...isObjectIdOrHexStrin
    }))
}
import mongoose from "mongoose";
const Schema = mongoose.Schema;

const exerciseSchema = new Schema({
  name: { type: String, required: true },
  image: String,
  description: String,
  category: String,
});


const Exercise = mongoose.model("Exercise", exerciseSchema);
export default Exercise;


const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const ejs = require('ejs');
const mongoose = require("mongoose");
const session = require('express-session');
const passport = require("passport");
const passportLocalMongoose = require("passport-local-mongoose");
const findOrCreate = require('mongoose-findorcreate');



const app = express();
const port = 5000;

// Use bodyParser middleware to parse JSON data
app.use(express.static("public"));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(session({
  secret: "Our little secret.",
  resave: false,
  saveUninitialized: false
}));

app.set('view engine', 'ejs');


// Enable CORS
app.use(cors());

app.use(passport.initialize());
app.use(passport.session());

mongoose.connect("mongodb://127.0.0.1:27017/healthcare", {useNewUrlParser: true, useUnifiedTopology: true });
// mongoose.set("useCreateIndex", true);

const userSchema = new mongoose.Schema ({
    username: String,
    password: String,
    desease: String
});
userSchema.plugin(passportLocalMongoose);
userSchema.plugin(findOrCreate);

const User = new mongoose.model("User", userSchema);

passport.use(User.createStrategy());

passport.serializeUser(function(user, done) {
  done(null, user.id);
});

passport.deserializeUser(function(id, done) {
  User.findById(id).then(function(user) {
    done(null, user);
  }).catch(function(err) {
    done(err, null);
  });
});


app.get("/", function(req, res){
  res.render("login");
});

app.get("/register", function(req, res){
  res.render("register");
});


// app.get("/logout", function(req, res){
//   req.logout();  
//   res.redirect("/");
// });

app.get("/logout", function(req, res){
  req.session.destroy(function(err) {
    res.redirect("/");
  });
});


app.get("/index",function(req,res){
  res.render("index");
});

app.get("/chatwithus",function(req,res){
  res.render("chatwithus");
});

app.get("/aboutUS",function(req,res){
  res.render("aboutUS");
});

app.get("/havesymptoms",function(req,res){
  res.render("havesymptoms");
});

app.get("/ourServices",function(req,res){
  res.render("ourServices");
});

app.post("/register", (req, res) =>{

  User.register({username: req.body.username}, req.body.password, function(err, user){
    if (err) {
      console.log(err);
      res.redirect("/register");
    } else {
      passport.authenticate("local")(req, res, function(){
        res.redirect("/index");
      });
    }
  });

});

app.post("/", function(req, res){

  const user = new User({
    username: req.body.username,
    password: req.body.password
  });

  req.login(user, function(err){
    if (err) {
      console.log(err);
    } else {
      passport.authenticate("local")(req, res, function(){
        res.redirect("/index");
      });
    }
  });

});

// Define the endpoint for prediction
app.post('/prediction', (req, res) => {
  // Process the received JSON data
  const values = req.body.values;

  // Replace this with your actual prediction logic
  const predictionResult = `Predicted result for values: ${values.join(', ')}`;

  // Send the prediction result as JSON response
  res.json({ prediction: predictionResult });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

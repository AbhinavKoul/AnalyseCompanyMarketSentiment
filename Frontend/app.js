const express= require("express");
var app= express();
var ejs = require('ejs');
var path=require("path");
var methodOverride = require("method-override");
const bodyParser = require("body-parser");
const { request } = require("http");
const axios=require('axios');

app.use(express.static(path.join(__dirname,'public')));
app.use(bodyParser.urlencoded({extended:true}));
app.use(methodOverride("_method"));

app.set('view engine', 'ejs');

app.get("/",function(req,res){
    res.render("home.ejs");
});

app.get("/explore",function(req,res){
    res.render("explore.ejs");
});


// app.get("/companypage/:id",function(req,res){
//     var comp='ITC';
//     const id = req.params.id;
//     console.log(comp+id);
//     res.render("companypage.ejs",{company:comp});
//     //res.render("Companypage.ejs");
// });
app.post("/companypage",function(req,res){
    var input= req.body.input;
    
    console.log(input);
    res.render("companypage.ejs",{company:input});
});

app.get("/companypage/:id",function(req,res){
    const id = req.params.id;
    console.log((id));
    if(id==1) comp="Reliance"
    if(id==2) comp="HDFCBANK"
    if(id==3) comp="TCS"
    if(id==4) comp="NTPC"
    if(id==5) comp="AXISBANK"
    if(id==6) comp="BPCL"
    if(id==7) comp="HAL"
    if(id==8) comp="IRCTC"
    if(id==9) comp="ICICIBANK"
    if(id==10) comp="ITC"

    res.render("companypage.ejs",{company:comp,company_id:id});

    
});

app.listen("3100",function(req,res){
    console.log("Server started");
});



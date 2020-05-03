var express =   require("express");
var multer  =   require('multer');
var app         =   express();

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './uploads');
  },
  filename: function (req, file, callback) {
    callback(null, 'Resume.pdf');
  }
});
var upload = multer({ storage : storage}).single('userPhoto');

app.get('/',function(req,res){
      res.sendFile(__dirname + "/index.html");
});

app.post('/api/photo',function(req,res){
    upload(req,res,function(err) {
        if(err) {
            return res.end("Error uploading file.");
        }
        
    });
});

app.get('/getResume',(req,res)=>{
    var spawn = require("child_process").spawn;
    var process = spawn('python',["./resPars.py"])
    process.stdout.on('data', function(data) { 
        res.send(data.toString()); 
        console.log(data.toString());
    })
});

app.listen(3000,function(){
    console.log("Working on port 3000");
});
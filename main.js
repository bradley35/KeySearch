var full_text="";
var all_data = [];
jQuery.get('text.txt', function(data) {
   full_text=data;
    run(0,0);
});
function getLineofText(beggining){
        return full_text.split("\n")[beggining]+" ";//.match(/^.{47}\w*/);
    
}

var before = 0;
function whichone(beggining){
    var count = 0;
    all = full_text.split("\n")
    for(var i=0; i<all.length; i++){
        before=count;
        count+=all[i].length+1;

        if(beggining<count){
            return i;
        }
    }
}
function run(beggining, wrong){
    
    var text=getLineofText(whichone(beggining));//[0];
    beggining = beggining-before;
    var start = text.lastIndexOf(" ", beggining)+1;
    
    if(start==-1){
        
        start=0;
    }
    //alert(start);
    var end = text.indexOf(" ", beggining)-1;
    if(end < 0){
        end = text.length;
    }
    if(start>end){
        start = start-1;
    }
    if(wrong<=0){
        document.getElementById("words").innerHTML="<p class='already'>"+text.substr(0,start)+"</p>"+
        "<p class='already current_word'>"+text.substr(start,beggining-start)+"</p>"+
        "<p class='current_letter current_word'>"+text.substr(beggining,1)+"</p>"+
        "<p class='current_word'>"+text.substr(beggining+1,end-beggining)+"</p>"+
        "<p class='rest'>"+text.substr(end+1)+"</p>";
    }else{
        document.getElementById("words").innerHTML="<p class='already'>"+text.substr(0,start)+"</p>"+
        "<p class='already current_word'>"+text.substr(start,beggining-start)+"</p>"+
        "<p class='current_word wrong'>"+text.substr(beggining,wrong)+"</p>"+
        "<p class='current_word'>"+text.substr(beggining+wrong,end-beggining-wrong+1)+"</p>";
        if(wrong<(end-start)){
            document.getElementById("words").innerHTML+="<p class='rest'>"+text.substr(end+1)+"</p>";
        }else{
            document.getElementById("words").innerHTML+="<p class='rest'>"+text.substr(beggining+wrong)+"</p>";
        }
        
    }
    if(text.indexOf("DONE")==0){
        name = prompt("You are finished! Nice Job. Please enter your name below: ", "");
        let csvContent = "data:text/csv;charset=utf-8,";
        all_data.forEach(function(rowArray){
            let row = rowArray.join(",");
            csvContent += row + "\r\n";
        }); 
        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", name.replace(" ", "_")+"_data.csv");
        document.body.appendChild(link);
        link.click();
    }
    
}
function findFirstDiffPos(a, b)
{
  var longerLength = Math.max(a.length, b.length);
  for (var i = 0; i < longerLength; i++)
  {
     if (a[i] !== b[i]) return i;
  }

  return -1;
}
function go(){
    typed=document.getElementById("enter").value;
    var re = new RegExp("\n", 'g');
    diff = findFirstDiffPos(full_text.replace(re, " "), typed);
    wrong = typed.length - diff;
    if(wrong>0){
        console.log("WRONG")
    }
    run(diff, wrong);
    if(wrong<=0){
        all_data.push([typed.slice(-1),new Date().getTime()]);
    }else{
        all_data.push(["E:"+typed.slice(-1), new Date().getTime()]);
    }

}
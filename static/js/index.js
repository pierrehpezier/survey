//Global:
var survey = []; //Bidimensional array: [ [1,3], [2,4] ]

//Switcher function:
$(".rb-tab").click(function(){
  //Spot switcher:
  $(this).parent().find(".rb-tab").removeClass("rb-tab-active");
  $(this).addClass("rb-tab-active");
});

$(".trigger").click(function(){
  survey = [];
  for (i=0; i<$(".rb").length; i++) {
    var rb = "rb" + i;
    var rbValue = parseInt($("#rb-"+i).find(".rb-tab-active").attr("data-value"));
    survey.push(rbValue); //Bidimensional array: [ [1,3], [2,4] ]
  };
  const Http = new XMLHttpRequest();
  Http.open("POST", "/response");
  Http.send(survey);
  alert("Envoyé!")
  //Debug:
  //debug();
});

//Debug:
function debug(){
  var debug = "";
  for (i=0; i<survey.length; i++) {
    debug += "Nº " + survey[i][0] + " = " + survey[i][1] + "\n";
  };
  alert(debug);
};

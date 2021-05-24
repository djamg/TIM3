function getEvents() {
    var cal = CalendarApp.getCalendarById("**********");
    var currentTime = new Date();
    var fcurrentTime = Utilities.formatDate(currentTime, "IST", "HH:mm:ss");
    var tenHoursFromNow = new Date(currentTime.getTime() + (18 * 60 * 60 * 1000));
    var events = cal.getEvents(currentTime, tenHoursFromNow);
    var afcurrentTime = fcurrentTime.split(':');
    var minutes2 = (+afcurrentTime[0]) * 60 + (+afcurrentTime[1]);
  
    
  
    if(events.length>0){
      var title = events[0].getTitle();
      var startTime = events[0].getStartTime();
      var fstartTime = Utilities.formatDate(startTime, "IST", "HH:mm");
      var afstartTime = fstartTime.split(':');
      //Logger.log(title + " " + fstartTime);
      var minutes1 = (+afstartTime[0]) * 60 + (+afstartTime[1]);
      var timeDiff = parseInt(minutes1)-parseInt(minutes2);
      //var xtimeDiff = fstartTime - xtime;
      
      //var timeToString = startTime.toTimeString().split(' ')[0];
      var epoch = ((startTime.getTime())/1000).toFixed(0);
      var epochOffset = parseInt(epoch);
      
      Logger.log(tenHoursFromNow);
      Logger.log(title);
      Logger.log(minutes1);
      Logger.log(minutes2);
      Logger.log(timeDiff);
      Logger.log(epochOffset);
      
   
    }
       
      
    //Logger.log(fcurrentTime);
    var data = {
         
        "title" : title,
        "request_source" : "gcal",
        "meta": "",
        "time_added" : fcurrentTime,
        "time_end" : epochOffset,
      
  };
    
    var options = {
    'method' : 'post',
    'contentType': 'application/json',
    // Convert the JavaScript object to a JSON string.
    'payload' : JSON.stringify(data)
  };
    
    
    if (timeDiff > 0) {
      
      UrlFetchApp.fetch('http://869b504f4449.ngrok.io/api/store', options);
    }
    else if (timeDiff<=0){
      Logger.log("Number is negative")
    }
    else{
      Logger.log("There is no event")
    }
  
  }
  
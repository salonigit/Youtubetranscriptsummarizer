chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.action == "initializeSummary") {
      chrome.tabs.query({active: true, lastFocusedWindow: true}, (tabs) => {
        if (tabs[0] == null) {
          chrome.runtime.sendMessage({action: "respondToButton", result: "Not a youtube video"});
          return;
        }
        var videoId = tabs[0].url.match('(?<=watch[?]v=).{11}');
        if (videoId != null) {
          // console.log(videoId[0]);
          chrome.runtime.sendMessage({action: "respondToButton", result: "Summary is being generated. Please wait!!"});
          window.open(
            "http://127.0.0.1:8000/Api/check/"+ videoId, "_blank" , "toolbar=yes,scrollbars=yes,resizable=yes,top=500,left=500,width=400,height=400");
        
        } else {
          chrome.runtime.sendMessage({action: "respondToButton", result: "Not a youtube video"});
        }
      });
    }
});
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
   // since only one tab should be active and in the current window at once
   // the return variable should only have one entry
   var activeTab = tabs[0];
   var url = activeTab.url;
   $.ajax({
     type: "POST",
     url: "http://127.0.0.1/detect",
     data: {data: url},
     success: function(data){removeElements(data, activeTab);},
   });
});

function removeElements(elements, activeTab) {
  console.log(elements);
  chrome.tabs.executeScript({
    code: '(' + function(params) {
        console.log(params);
        var replaceImage = document.createElement('img');
        replaceImage.src = 'https://i.imgur.com/RKDokkU.png';

        if (params['videos'] && params['videos'] == true) {
          console.log('bruh');
          var el = document.getElementById("movie_player");
          el.parentNode.replaceChild(replaceImage, el);
        }

        if (params['paragraphs'].length > 0) {
          var pars = document.getElementsByTagName('p');
          pars[0].parentNode.replaceChild(replaceImage, pars[0]);
          pars = document.getElementsByTagName('p');
          while(pars.length != 0) {
            pars[0].remove();
          }
        }

        if (params['images'].length > 0) {
          var pars = document.getElementsByTagName('img');
          while(pars.length != 0) {
            pars[0].remove();
          }
        }

        return {success: true, html: document.body.innerHTML};
    } + ')(' + JSON.stringify(elements) + ');'
  }, function(results) {
    console.log(results[0]);
  });
  chrome.browserAction.setBadgeText({
    text: "" + elements["length"], 
    tabId: activeTab.id
  });
  window.close();
}
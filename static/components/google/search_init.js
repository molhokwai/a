/* requires <script 
    src="http://www.google.com/jsapi?key=ABQIAAAAhDaHyndn3TRHW8aVVgNfsBTPFwiohxerrbIfi_L7lDZ1YENwhRROxgxsy_RTT4IRmc8SWIpWu3KrsQ" type="text/javascript"></script> */
var google_search_load=function() {
    google.load("search", "1");
    
    molhokwai['google']= {
          search : {
            control : null,
                onload : 
                  function (){
                    // Create a search control
                    var m_g_s_c = new google.search.SearchControl();
    
                    // Add in a full set of searchers
                    var localSearch = new google.search.LocalSearch();
                    m_g_s_c.addSearcher(localSearch);
                    m_g_s_c.addSearcher(new google.search.WebSearch());
                    m_g_s_c.addSearcher(new google.search.VideoSearch());
                    m_g_s_c.addSearcher(new google.search.BlogSearch());
                  
                    // Set the Local Search center point
                    localSearch.setCenterPoint("Rue Sneessens 1, 1040 Etterbeek, Belgium");
                  
                    // Tell the searcher to draw itself and tell it where to attach
                    m_g_s_c.draw(document.getElementById("searchcontrol"));
                    molhokwai.google.search.control=m_g_s_c;
                },
    
            response : {
              get : 
                function (value){
                  // Execute a search
                  molhokwai.google.search.control.execute(value);
              }
            }
          }
        };
        
    google.setOnLoadCallback(molhokwai.google.search.onload);
    setTimeout('molhokwai.google.search.onload();', 100);
    
    return true;
};

        try {
        // for Node.js
        var autobahn = require('autobahn');
        } catch (e) {
        // for browsers (where AutobahnJS is available globally)
        }

        var connection = new autobahn.Connection({url: 'ws://172.16.42.2:9000/ws', realm: 'tf_cb_router'});

        var session;

        function addGW() {
            var gw_name = $('input[name="gw_name"]').val();
            var gw_ip = $('input[name="gw_ip"]').val()
            console.log("Name:", gw_name)
            console.log("IP:", gw_ip)

        }

        function genItemList(args) {
            console.log("inside genItemList")
            session.call('com.portier.get_networks').then(
                function (res) {
                    console.log("Result0:", res[0,1]);
                    console.log("Result1:", res[1,1]);


                    var newEL = document.createElement("div")
                    newEL.setAttribute('class', 'dropdown-menu show')
                    newEL.setAttribute('aria-labelledby', 'navbarDropdownMenuLink')
                    newEL.setAttribute('id', 'dropdown-network')

                    res.forEach(function (item, index) {
                        console.log(item, index)
                        var tag = document.createElement("a")
                        tag.setAttribute('class', 'dropdown-item')
                        tag.setAttribute('href', "#")
                        tag.textContent = item
                        newEL.appendChild(tag)
                    });

                    console.log(newEL)
                    var element = document.getElementById("dropdown-network");
                    console.log(element)
                    element.parentNode.replaceChild(newEL, element);
                }
            );


        }

        connection.onopen = function (new_session) {


        session = new_session;

        // 1) subscribe to a topic
        function onevent(args) {
            console.log("Event:", args[0]);
            jQuery("#status").html(args[0]);
        }
        session.subscribe('com.topic.portier.status', onevent);

        // 2) publish an event
        session.publish('com.topic.portier.status', ['Hello, world!']);

        // 3) register a procedure for remoting
        function add2(args) {
            return args[0] + args[1];
        }
        // session.register('com.myapp.add2', add2);

        // 4) call a remote procedure
        //function genitemlist(args) {
        //    session.call('com.topic.portier.web.getNetworks').then(
        //        function (res) {
        //            console.log("Result:", res);
        //        }
        //    );
        //}
        };

        connection.open();

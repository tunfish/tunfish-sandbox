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
        session.register('com.myapp.add2', add2);

        // 4) call a remote procedure
        session.call('com.myapp.add2', [2, 3]).then(
            function (res) {
                console.log("Result:", res);
            }
        );
        };

        connection.open();

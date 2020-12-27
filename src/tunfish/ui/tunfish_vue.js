
        try {
        // for Node.js
        var autobahn = require('autobahn');
        } catch (e) {
        // for browsers (where AutobahnJS is available globally)
        }

        var connection = new autobahn.Connections

        var session;


        connection.onopen = function (new_session) {

            session = new_session;
            startApp();

        };

        function startApp() {
            var app = new Vue({
                el: '#app',
                data:{
                    networks: ["nw1", "nw2"]
                },

                methods: {
                    getNetworkList: function (event) {
                        console.log("inside getNetworkList")
                        console.log(this.networks)

                        var list = []

                        session.call('com.portier.get_networks').then(
                            function (res) {
                                console.log(res)
                                res.forEach( function (item, index) {
                                    console.log(item, index)
                                    list.push(item)
                                    console.log(list)
                                })
                                console.log(res)
                            }
                        )

                        this.networks = list
                    },

                    getNetworkData: function (event){
                        console.log("inside getNetworkData")
                        console.log(event)

                    },

                    addNetwork: function (event){
                        console.log("inside addNetwork")
                    }
                }
            })
        }



        connection.open();

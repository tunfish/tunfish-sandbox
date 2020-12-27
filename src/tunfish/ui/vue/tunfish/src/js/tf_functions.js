try {
	// for Node.js
	// let autobahn = require('autobahn');
} catch (e) {
	// for browser (where AutobahnJS is avaiable globally)
}
//let autobahn = require('autobahn');
//let connection = new autobahn.Connection({url: 'ws://172.16.42.2:9000/ws', realm: 'tf_cb_router'});
//let session;

//connection.onopen = function(new_session) {
//	session = new_session;
//}


export const tf_functions = {

	doConnection: () => {
		console.log('inside doConnection')
		let autobahn = require('autobahn');
		let connection = new autobahn.Connection({url: 'ws://172.16.42.2:9000/ws', realm: 'tf_cb_router'});

		connection.onopen = function(new_session) {
			//this.$tf_variables.session = new_session;
			//tf_variables.session = new_session        try {

			this.$store.state.session = new_session
		}
	},

	getNetworkList: () => {
		console.log('inside getNetworkList')
		//this.$tf_functions.doConnection()
		this.store.commit('doConnection')
		let list = []
		//tf_variables.session.call('com.portier.get_networks').then(
		this.$store.state.session.call('com.portier.get_networks').then(
			function (res) {
				console.log(res)
				res.forEach(function (item, index) {
					console.log(item, index)
					list.push(item)
					console.log(list)
				})
				console.log(res)
			}
		)
		return list
	}
}
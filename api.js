// generate by acgt
var Api = {
  host: "",
  fetch_new_press: function(args, cb_success) {
    $.ajax({
      type: 'get',
      url: this.host + '/press/fetch_new_press',
      data: args,
      success: function(data) {
        cb_success(data);
      },
      error: function() {
        console.log("ajax error");
      },
      dataType: 'JSON'
    });
  },
  fetch_all: function(args, cb_success) {
    $.ajax({
      type: 'get',
      url: this.host + '/press/fetch_all',
      data: args,
      success: function(data) {
        cb_success(data);
      },
      error: function() {
        console.log("ajax error");
      },
      dataType: 'JSON'
    });
  },
}
openerp.optibiz = function(instance, local) {
    alert("Santosh is called");
    var MyClass = instance.web.Class.extend({
        sayHello: function() {
            console.log("Hello Called");
        }
    });

    var x = new MyClass();
    x.sayHello();
}
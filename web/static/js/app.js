var app = angular.module("app",['ngCookies']);

app.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('jqdatepicker', function () {
  return {
      restrict: 'A',
      require: 'ngModel',
       link: function (scope, element, attrs, ngModelCtrl) {
          element.datepicker({
              dateFormat: 'DD, d  MM, yy',
              onSelect: function (date) {
                  scope.date = date;
                  scope.$apply();
              }
          });
      }
  };
});

app.controller('login', function($scope,$http,$cookies) {
    $scope.username = "";
    $scope.password = "";

    var token=$cookies.get('token');
    var role=$cookies.get('user');

    if(token === ""){
        if(role=="admin"){
            window.location.href = "dashboard/";
        }
        else{
            window.location.href = "task/";
        }
    }

    $scope.onSubmit = function(){
        
        $http.post("/api/v1/login",data={"username":$scope.username,"password":$scope.password}).then(function (response) {

            // This function handles success
            if(response.status==200){
                //set cookie
                $cookies.put('token',response.data.data.token);
                
                if(response.data.data.staff){
                    $cookies.put('role',"admin");
                    window.location.href = "dashboard/";
                }
                else{
                    $cookies.put('role',"employee");
                    window.location.href = "task/";
                }
                
            }
            
            }, function (response) {
            
            // this function handles error
        
        });
    }
    
});

app.controller('task', function($scope,$http,$cookies,$location) {
    
    $scope.tasks = [];
    
    $scope.taskName = "";
    $scope.date = "";

    //get cookie
    var token=$cookies.get('token');
    $http.defaults.headers.common['Authorization'] = 'Token '+token;
    
    //Get all tasks
    $http.get("/api/v1/task").then(function (response) {
        console.log("Task:",response.data.data);
        if(response.status==200){
            
            console.log("Task details:",response.data);
            for(var i=0;i<response.data.data.length;i++){
                $scope.tasks.push(response.data.data[i]);
            }
        }
        }, function (response) {
            
            console.log("Error:",response);
    });
    
    $scope.onAdd = function(){

        console.log($scope.taskName,$scope.date);
        $http.post("/api/v1/task",data={"task_name":$scope.taskName}).then(function (response) {
            if(response.status==201){
                console.log("Task created");
                $scope.tasks.push(response.data.data);
                $scope.taskName = "";
            }
            }, function (response) {
                
                console.log("Error:",response);
        });
    }

    $scope.loadNotifications = function(){
        $http.get("/api/v1/notification").then(function (response) {
            console.log("Task:",response.data.data);
            if(response.status==200){
                console.log("Notifications:",response.data);
                for(var i=0;i<response.data.data.length;i++){
                    $scope.notifications.push(response.data.data[i]);
                }
            }
            }, function (response) {
                
                console.log("Error:",response);
        });
    }

    $scope.updateProgress = function(taskId){
        $http.patch("/api/v1/task",data={"id":taskId,"task_status":"CP"}).then(function (response) {
            console.log("Task:",response.data.data);
            for(var j=0;j<$scope.tasks.length;j++){
                console.log("Task:",$scope.tasks[j],$scope.tasks[j].id,$scope.tasks[j]['id']);
                if($scope.tasks[j].id == response.data.data['id']){
                    $scope.tasks[j].task_status = response.data.data['task_status']
                }
            }
            }, function (response) {
                console.log("Error:",response);
        });
    }

    $scope.onLogout = function(){
        
        $cookies.remove('token');
        $cookies.remove('user');
        
        window.location.href="/";
    }
    
});


app.controller('dashboard', function($scope,$http,$cookies) {
    
    $scope.tasks = [];
    $scope.notifications = [];
    $scope.comments = [];
    $scope.newComment = "";

    //get cookie
    var token=$cookies.get('token');
    $http.defaults.headers.common['Authorization'] = 'Token '+token;

    
    //Get all tasks
    $http.get("/api/v1/task").then(function (response) {
        if(response.status==200){
            
            console.log("Task details:",response.data);
            for(var i=0;i<response.data.data.length;i++){
                $scope.tasks.push(response.data.data[i]);
            }
        }
        
        }, function (response) {
            
            console.log("Error:",response);
    });

    $http.get("/api/v1/notification").then(function (response) {
        console.log("Task:",response.data.data);
        if(response.status==200){
            console.log("Notifications:",response.data);
            for(var i=0;i<response.data.length;i++){
                $scope.notifications.push(response.data[i]);
            }
        }
        }, function (response) {
            
            console.log("Error:",response);
    });

    $scope.onCommentAdd = function(taskId,comment){
        $http.post("/api/v1/comment",data={"task":taskId,"comment":comment}).then(function (response) {
            if(response.status==201){
                $scope.newComment ="";
                console.log("Comment created:",response.data);
                for(var j=0;j<$scope.tasks.length;j++){
                    console.log("Task:",$scope.tasks[j],$scope.tasks[j].id,$scope.tasks[j]['id']);
                    if($scope.tasks[j].id == response.data.data['task']){
                        $scope.tasks[j].Tasks_Comments.push({"task":taskId,"comment":response.data.data['comment']})
                    }
                }
            }
            }, function (response) {
                
                console.log("Error:",response);
        });
    }

    $scope.onLogout = function(){
        $cookies.remove('token');
        $cookies.remove('user');
        window.location.href="/";
    }

});
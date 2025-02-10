const TodoApp = angular.module("TodoListApp", ["ngRoute"])

const BASE_URL = "/ui"
const TEMPLATE_PATH = "/template"
const BACKEND_URL = "http://127.0.0.1:8000/todos/api"

// WARNING: For development only
const HTTP_CONFIG = {
    url: "http://127.0.0.1:8000/todos/api",
    headers: {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Authorization": "Basic Y2FsdmluOmNhbHZpbg==", // Only use because there are no login feature for this app yet
    }
}

const navList = [
    {
        text: "Dashboard",
        icon: "dashboard",
        href: "/",
        template: "/dashboard.html",
    },
    {
        text: "All Todos",
        icon: "list",
        href: "/list",
        template: "/list.html",
    },
]

TodoApp.config(($routeProvider, $locationProvider) => {
    $locationProvider.html5Mode(true)
    
    navList.forEach((list) => {
        $routeProvider
            .when((BASE_URL + list.href), {
                templateUrl: BASE_URL + TEMPLATE_PATH + list.template
            })
    })

    $routeProvider.otherwise({
        redirectTo: "/"
    })
})

TodoApp.controller("AppController", ($scope, $location, $http) => {
    $scope.currentLocationPath = $location.path()
    $scope.navList = navList

    $scope.newNote = {
        note: "",
        due_date: ""
    }

    $scope.todayList = []

    $http({
        method: "GET",
        ...HTTP_CONFIG
    }).then((res) => {
        $scope.todayList = res.data
    })

    $scope.addNewList = () => {
        HTTP_CONFIG.headers["Content-Type"] = "application/json"
        const due_date = $scope.newNote.due_date.toISOString().split('T')[0]

        $http({
            method: "POST",
            data: {
                note: $scope.newNote.note,
                due_date: due_date,
            },
            ...HTTP_CONFIG
        }).then((res) => {
            if(res.status == 200) {
                location.reload()
            }
        }).catch((err) => {
            alert("Failed to save new note")
        })

        $scope.newNote = {
            note: "",
            due_date: ""
        }
    }

    $scope.finishNote = (id) => {
        HTTP_CONFIG.url = HTTP_CONFIG.url + `/${id}`
        $http({
            method: "PUT",
            data: {
                is_complete: true,
            },
            ...HTTP_CONFIG
        }).then((res) => {
            if(res.status == 200) {
                alert("Data successfully updated")
                location.reload()
            }
        }).catch((err) => {
            alert("Data failed to update")
        })
    }

    $scope.deleteNote = (id) => {
        HTTP_CONFIG.url = HTTP_CONFIG.url + `/${id}`
        $http({
            method: "DELETE",
            ...HTTP_CONFIG
        }).then((res) => {
            if(res.status == 200) {
                alert("Data has been deleted")
            } 
        }).catch((err) => {
            alert("Data delete failed")
        })
    }

    $scope.$on("$routeChangeSuccess", () => {
        $scope.currentRoute = $location.path();
    });
})
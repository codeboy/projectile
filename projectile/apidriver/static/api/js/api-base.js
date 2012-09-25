jQuery(document).ajaxSend(function(event, xhr, settings) {
    var csrf_token = $('#csrf-token').val();
//    console.log(csrf_token);
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
});


/*****************************************************
 *   стартовый скрипт для админ панели
 *
 * TODO: добавить создание словарей табов (панели и контента) на инит
 * TODO: сделать поиск по табам нормальным
 * TODO: есть непорядок с областями видимости - надо разобраться
 * TODO: переделать tooltips
 *
 *****************************************************/

BaseApp = function(){
    this.params = {};

    this.init = function (params) {
        var params = $.extend({}, this.params, params);
        var a = this;

        a.$content = $('#content');

        // меню
        a.$menuList = $('#sidebar');
        a.$menuListItems = $('#sidebar a');

        a.$urlList = urlList;
        a.$currentUrl = $(location).attr('hash');

        this.starterLoadContent();
        this.bindEvents();

        //this.testAjax();
        //$('.tabListContainer li').on('click', function(e){baseApp.tabClick(e)});
    };

    /**
     *   EVENTS & ACTIVATORS
     *******************************************************/
    this.bindEvents = function() {
        //this.openerTriggerList.live('click', function() {});

        baseApp.disableLoader();

        this.$menuListItems.on('click', baseApp.menuClick);

        $(window).on('click', '.loader', baseApp.contentLoader);

//        $('.loader').on('click', function(e){
//            baseApp.contentLoader();
//        });
        //$('div.startalert').click(function (){ baseApp.createAlert('title2', 'content2') });

    };

    /********************************************
     *  FUNCTIONS
     *******************************************/
    this.cl = function(content) {
        content = content == undefined ? 'Warning' : content
        console.log(content)};
    /**
         * hide \ show loader
         **************************************/
        this.disableLoader = function() {
            $('#loading-mask, #loading').hide();
    //        this.$viewport.show();
        };
        this.enableLoader = function() {
            $('#loading-mask, #loading').show();
    //        this.$viewport.show();
        };

    /**
     * load actual content based on page url
     * page urls temporary stored in menu tpl (ba-inc-menu.html)
     */
    this.starterLoadContent = function(){
        var url = 'api-test/test';
        var urls = baseApp.$urlList;
        var current_url = baseApp.$currentUrl;
        current_url = current_url.substr(1);

        var current_url_array = current_url.split('/');
        current_url = current_url_array[0];

        if (current_url_array.length > 1) {
            if (current_url_array[0] == 'project') {
                url = '/api-project/project/'+current_url_array[1];
                baseApp.makeMenuActive('projects');
            }
        } else {
            if (current_url in urls){
                console.log('load content for - ', current_url);
                url = urls[current_url];
                baseApp.makeMenuActive(current_url);
            }
        }
        var callback = function(data) {
            baseApp.reloadContent(data.data);
        };
        var r_data = baseApp.getContent(url, callback);
    };


    /**
     * make menu element active
     * @param url
     *************************************/
    this.makeMenuActive = function(url){
        var menu = baseApp.$menuList;
        var menuActiveItem = menu.find('li.active');
        menuActiveItem.removeClass('active');

        var dash = url.slice(0,1);
        if (dash === '#') {}
        else {url = '#'+url}

        var menuItemToActivate = menu.find('li > a[href*='+url+']');
        menuItemToActivate.parent().addClass('active');

    };


    /**
     * клик по элементу меню
     ******************************************/
    this.menuClick = function(event) {
//        event = event || window.event;
//        var me = $(event.target);
        var me = $(this);
        var me_turl = me.data('turl');

        var callback = function(data) {
            console.log('ajax data', data);
            baseApp.reloadContent(data.data);
            baseApp.makeMenuActive(me.attr('href'));
        };
        var r_data = baseApp.getContent(me_turl, callback);

//        return false;
    };

    this.contentLoader = function() {
        var me = $(event.target);
        var me_tag = String(me.prop("tagName").toLowerCase());
        if (me_tag == 'span'){
            me = me.parent();
        }
        var me_turl = me.data('turl');
        console.log('me_turl', me_turl);

        var callback = function(data) {
            baseApp.reloadContent(data.data);
        };
        var r_data = baseApp.getContent(me_turl, callback);
    };

    /**
     * reload page content
     * @param data
     */
    this.reloadContent = function (data){
        this.$content.html(data);
    };

    /**
     * get script sended in request
     * @param script
     */
    this.getScript = function(script){
        $.ajax({
            url: '/static/'+script,
            dataType: "script",
            success: function(data, textStatus, jqxhr){
            },
            error:function(data, textStatus, jqxhr){
                console.log('data', data); //data returned
                console.log('textStatus', textStatus); //success
                console.log('jqxhr.status', jqxhr.status); //200
                console.error('Load was canceled.');
                baseApp.createAlert('Ошибка', 'Ошибка загрузки javascipt ('+(Math.floor(Math.random() * (1000 - 1 + 1)) + 1)+'): '+script);
            }
        });
        //$.getScript('/static/ap/js/'+script, function(data, textStatus, jqxhr) {
    };


    // ! deprecated
    this.testAjax = function(){
        $.ajax({
            url: 'api/testajax/',
            type: 'POST',
            success: function(data) {
                console.log(data);
                return data
            },
            error: function(data, textStatus, jqxhr){
                console.log('data', data); //data returned
                console.log('textStatus', textStatus); //success
                console.log('jqxhr.status', jqxhr.status); //200
                console.error('Load was canceled.');
                baseApp.createAlert('Ошибка', 'Произошла ошибка');
            }
        });
    };

    /**
     * загрузка контента
     * @param url
     * @param callback
     */
    this.getContent = function(url, callback){
        baseApp.enableLoader();
        $.ajax({
            url: baseApp.frontSlash(url),
            type: 'POST',
            success: function(data) {
                baseApp.disableLoader();
                console.log('get requested!');
                callback(data);
                //return data;
            },
            error: function(data, textStatus, jqxhr){
                baseApp.disableLoader();
                console.log('data', data); //data returned
                console.log('textStatus', textStatus); //success
                console.log('jqxhr.status', jqxhr.status); //200
                console.error('Load was canceled.');
                baseApp.createAlert('Ошибка', 'Произошла ошибка при загрузке данных с: '+url, 'error');
            }
        });
    };
    /**
     * добавляет слеш к урлу
     * @param url
     * @return {*}
     */
    this.frontSlash = function(url) {
        var slash = url.slice(0,1);
        if (slash === '/') { return url }
        else {return '/'+url}
    };

    /**
     * перезагрузка данных во вкладке
     * @param data
     * @param cache
     */
    this.tabReload = function(data, cache){

        // TODO: rebuild tooltip system
        $('span.tp').tooltip('hide');
        $('a.tp').tooltip('hide');

        cache = cache == undefined ? 0 : cache;
        var tabContainer = $('#tabBody');
        var me = tabContainer.find('li.active');
        me.html(data);
    };


    // для тестового вызова из стороннего скрипта
    this.testAlert = function() {
        console.log('They call me!');
    };

    /**
     * создаёт всплывающий алерт
     * @param title
     * @param content
     * @param type - тип алерта error, block, success
     */
    this.createAlert = function(title, content, type) {
        title = title == undefined ? 'Warning' : title;
        content = content == undefined  ? '' : content;
        type = type == undefined  ? 'block' : type;

        var alertWindow = $('<div class="alert alert-'+type+'" id="alert-popup">'
            +'<a class="close" data-dismiss="alert" href="#">×</a>'
            +'<h4 class="alert-heading">'+title+'</h4>'
            +'<p class="alert-content">'+content+'</p></div>');
        alertWindow.appendTo($('div#alert-container'));
        //$('div#alert-container').append(alertWindow);
    };

    // deprecated
    this.paginationNext = function(){
        var me = $(this);
        console.log(me);
        var callback = function(r_data){
            console.log(r_data)
        }
        var data = baseApp.getTabContent(turl, create);
    };
    // deprecated
    this.paginationPrev = function(){
        console.log($(this));
    }
};



$(document).ready(function () {
    baseApp = new BaseApp();
    baseApp.init();
});

/*****************************************************
 * просто скрипт
 *****************************************************/

var TabTest = {
    init: function() {
        console.log('start init TabTest');
        baseApp.testAlert();

        this.cacheElements();
        this.bindEvents();
        this.render();


    },

    // создание \ кэш элементов и данных в ап и\или в локалстор
    cacheElements: function() {},

    /**
     *  устанавливаем обработчики событий
     */
    bindEvents: function() {
        $(document).on('click', 'div.test-alert', function(){
            baseApp.createAlert('Ну нифигассе!', 'у тебя получилось!', 'success');
        });
        $(document).on('click', 'div.test-reload', this.reloadContent);
    },

    // сам рендер темплейта (т.е. весь пререндер)
    render: function() {},

    reloadContent: function() {
        console.log('start reload');

        var callback = function(data) {
            console.log('reloaded');
            baseApp.tabReload(data.data);
        };

        baseApp.getTabContent('api-test/reload-test', callback)
    }

};
jQuery(function( $ ) {
    TabTest.init();
});

import pyjd # this is dummy in pyjs.
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextArea import TextArea
from pyjamas.HTTPRequest import HTTPRequest
from pyjamas import Window
from pyjamas.JSONService import JSONProxy
import pygwt
location = Window.getLocation()


def locationObjPanel():
    vpl = VerticalPanel();
    vpl.add(HTML(location.getPageHref(self)))
    vpl.add(HTML(location.getSearchVar('theme')))
    vpl.add(HTML(location.getSearch(self)))
    return vpl

# async request
class HTTPAsyncRequestHandler:
    """
        Usage: 
            -   Instantiation
            -   Subclassing:
            In both cases setting (texts, messagePanels), and/or (callbacks) parameter(s)
            in construction or through attributs
    """
    caller = None
    callbacks = None
    def __init__(self, caller, callbacks): 
        self.caller = caller
        self.callbacks = callbacks

    def onCompletion(self, text):
        if self.callbacks and 'onCompletion' in self.callbacks:
            self.callbacks['onCompletion'](self.caller, text)

    def onError(self, text, code):
        if self.callbacks and 'onError' in self.callbacks:
            self.callbacks['onError'](self.caller, text, code)

    def onTimeout(self, text):
        if self.callbacks and 'onTimeout' in self.callbacks:
            self.callbacks['onTimeout'](self.caller, text)

class Index():
    texts = None
    callbacks = None
    urls = None

    def __init__(self):
        self.texts = {
            'themesRequest': {
                'onCompletion' : 'Themes fetched, displaying/displayed.',
                'onError' : 'An error occured fecthing themes, displaying static themes (error details - text:%s, code:%s)',
                'onTimeout' : 'Timed out fetching themes, displaying static themes (error details - text:%s)'
            }
        }
        self.callbacks = {
            'themesRequest': {
                'onCompletion' : Index.themesRequestOnCompletion,
                'onError' : Index.themesRequestOnError,
                'onTimeout' : Index.themesRequestOnTimeout
            }
        }
        self.urls = {
            'themesRequest': {
                'main' : "/a/default/json/themes"
            }
        }


    def messagePanel(self):
        return self.htmlElements()[1][1]

    def onModuleLoad(self):
        self.htmlElements()
        try:
            HTTPRequest().asyncGet(
                    self.urls['themesRequest']['main'], 
                    HTTPAsyncRequestHandler(self, self.callbacks['themesRequest'])
            )
        except Exception, ex:
            self.htmlElements()[1][1].add(HTML(str(ex)))


    def onTextAreaChange(textArea):
        textArea.setText(eval(textArea.getText()))

    _htmlElements = None
    def htmlElements(self, addList = None):
        if not self._htmlElements:
            h = HTML("<h1>Hello from %s</h1>" % location.getHref(), StyleName='font-s07em')
            p = HorizontalPanel(HTML('Valid/tested combinations'))
            grid = Grid(2,2)
            grid.setHTML(0, 0, "app")
            grid.setHTML(0, 1, "themes")
            grid.setHTML(1, 0, "a")
            grid.setHTML(1, 1, "0 - 1 - ff0000 - cms - pypress - wordpress")
            t = TextArea()
            t.addChangeListener(Index.onTextAreaChange)
            self._htmlElements = [['h', h], ['p', p], ['grid', grid], ['t', t]]   
            for i in range(len(self._htmlElements)):
                RootPanel().add(self._htmlElements[i][1])
        if addList:
            self._htmlElements+=addList
            for i in range(len(self._htmlElements)):
                RootPanel().add(addList[i][1])

        return self._htmlElements

    def toTheme(button):
        location.setSearchDict({'theme': button.getID()})

    def themesRequestOnCompletion(self, themes):
        self.messagePanel().add(HTML(self.texts['themesRequest']['onCompletion']))
        self.htmlElements(addList=[['tp', self.themesPanel(themes)]])
        
    def themesRequestOnError(self, text, code):
        self.messagePanel().add(HTML(self.texts['themesrequest']['onError'] % (text, code)))

    def themesRequestOnTimeout(self, text):
        self.messagePanel().add(HTML(self.texts['themesrequest']['onTimeout'] % (text)))

    def themesPanel(self, themes=None):
        themes = None
        if not themes: themes=['0','1', 'cms', 'pypress']
        
        vPanel = VerticalPanel()
        vPanel.setID('themes')
        for i in range(len(themes)):
            a=Button('theme %s' % themes[i], Index.toTheme, StyleName='link')
            a.setID(themes[i])
            vPanel.add(a)
    
        return vPanel


if __name__ == '__main__':
    pyjd.setup("public/Index.html")
    app = Index()
    app.onModuleLoad()
    pyjd.run()

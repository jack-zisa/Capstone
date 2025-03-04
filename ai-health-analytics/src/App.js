import './App.css';
import { TableauViz, TableauEventType } from "@tableau/embedding-api";
import { useRef, useEffect, useMemo } from 'react';

function App() {
  const vizRef = useRef(null);

  const eventHandlers = useMemo(() => [
    {
      eventType: TableauEventType.MarkSelectionChanged,
      handler: (event) => {
        console.log('Mark Selection Event', event);
      },
    },
  ], []);

  const options = useMemo(() => ({
    hideTabs: true,
    width: '100%',
    height: '100%',
  }), []);

  useEffect(() => {
    if (vizRef.current) {
      const viz = new TableauViz(vizRef.current, {
        url: 'https://public.tableau.com/views/IotDevices/Dashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link',
        options: options,
      });

      eventHandlers.forEach(({ eventType, handler }) => {
        viz.addEventListener(eventType, handler);
      });

      return () => {
        eventHandlers.forEach(({ eventType, handler }) => {
          viz.removeEventListener(eventType, handler);
        });
      };
    }
  }, [options, eventHandlers]);

  return (
    <div className="App">
      <header className="App-header">
        <div className='tableauPlaceholder' id='viz1741104901655' style={{position: 'relative'}}>
          <noscript>
            <a href='#'>
              <img alt='Dashboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Io&#47;IotDevices&#47;Dashboard&#47;1_rss.png' style={{border: 'none'}} />
            </a>
          </noscript>
          <object className='tableauViz'  style={{display: 'none'}}>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='IotDevices&#47;Dashboard' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Io&#47;IotDevices&#47;Dashboard&#47;1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
            <param name='filter' value='publish=yes' />
          </object>
        </div>
      </header>
    </div>
  );
}

export default App;

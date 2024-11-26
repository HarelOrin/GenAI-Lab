import ReactJsonView from 'react18-json-view'
import 'react18-json-view/src/style.css'


const decodeBase64ToJson = (base64String) =>  {
    const jsonString = atob(base64String);
    return JSON.parse(jsonString);
}

const RenderJson = ({src}) => {
 
    let schema = decodeBase64ToJson(src);

    if (typeof schema === 'string') {
        schema = JSON.parse(schema); 
      }

    return (
        <div>
            <ReactJsonView
                src={schema}
                theme="monokai"          
                collapsed={false}      
                enableClipboard={true}  
                displayDataTypes={true} 
                displayObjectSize={true} 
            />
        </div>
    )
}

export default RenderJson
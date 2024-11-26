import React, {useContext, useEffect} from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import nintexAvatar from '../../../../../assets/avatars/nintexAvatar.png'
import userAvatar from '../../../../../assets/avatars/userAvatar.png'
import '../ChatHistory.css'

const ChatHistory = ({ fieldData }) => {
    const { setInputValues, inputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    useEffect(() => {
        if (fieldData.history && fieldData.history.length !== 0 && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.history }));
        }
    }, [fieldData.history, inputValues, setInputValues, title]);

    return (
        <div className="history-container">
            <div className="history-center">
                <div className="messages-container">
                    {fieldData.history.map((message, index) => (
                        <div className={`message-container ${message.role}`}>
                            <img
                                src={message.role === 'user'
                                    ? userAvatar
                                    : nintexAvatar}
                                alt={message.role}
                                className={`message-icon ${message.role}`}
                            />
                            <div className={`message ${message.role}`}>                
                                <p dangerouslySetInnerHTML={{ __html: message.content }} />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default ChatHistory
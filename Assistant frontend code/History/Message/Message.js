import { v4 as uuidv4 } from 'uuid';
import React from 'react';
import PropTypes from 'prop-types';

import Feedback from './Feedback/Feedback';

import './Message.css';
import NintexAvatar from '../../../../assets/avatars/nintexAvatar.png';
import UserAvatar from '../../../../assets/avatars/userAvatar.png';

function Message({ message, isLastMessage }) {
	// Prop type validation
	Message.propTypes = {
		message: PropTypes.shape({
			id: PropTypes.number.isRequired,
			role: PropTypes.string.isRequired,
			content: PropTypes.string.isRequired,
			sources: PropTypes.arrayOf(
				PropTypes.shape({
					name: PropTypes.string,
					link: PropTypes.string,
				})
			),
		}).isRequired,
		isLastMessage: PropTypes.bool.isRequired,
	};

	const iconSrc = message.role === 'user'
		? UserAvatar
		: NintexAvatar;

	const formattedContent = message.content.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');

	//====================================================================================================
	//                                             <Message />
	//====================================================================================================
	return (
		<div className={`message-container ${message.role}`}>
			<img
				src={iconSrc}
				alt={message.role}
				className={`message-icon ${message.role}`}
			/>
			<div className={`message ${message.role}`}>                
				<p dangerouslySetInnerHTML={{ __html: formattedContent }} />

				{message.sources && (
					<div>
						<div>
							<hr />
							{message.sources.map((source) => (
								<a
									key={uuidv4()}
									href={source.metadata.source}
									target="_blank"
									rel="noopener noreferrer"
								>
									<p>{source.metadata.title} | {source.metadata.category}</p>
								</a>
							))}
						</div>
						<Feedback isLastMessage={isLastMessage} messageId={message.id} />
					</div>
				)}
			</div>
			
		</div>
	);
}

export default Message;

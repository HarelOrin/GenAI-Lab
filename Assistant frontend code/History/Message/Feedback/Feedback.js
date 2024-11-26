import React, { useState, useContext, useEffect } from 'react';
import { ChatContext, sendFeedback } from '../../../../../contexts';
import { useTranslation } from 'react-i18next';

import classNames from 'classnames';
import PropTypes from 'prop-types';

import './Feedback.css';

import WhatsWrong from './WhatsWrong/WhatsWrong';
import ToggleButtons from './ToggleButtons/ToggleButtons';

const Feedback = ({ isLastMessage, messageId }) => {
	Feedback.propTypes = { 
		isLastMessage: PropTypes.bool.isRequired,
		messageId: PropTypes.number.isRequired
	};

	const { t } = useTranslation();
	
	const [state, setState] = useState(null);
	
	// Handle transitions
	const [showText, setShowText] = useState(isLastMessage);
	const [transitionButtons, setTransitionButtons] = useState(!isLastMessage);
	const [showFeedback, _setShowFeedback] = useState(false);
	const [transitionOut, _setTransitionOut] = useState(!isLastMessage);
	const [renderThanks, _setRenderThanks] = useState(false);

	const { messages, setIsLastFeedbackOpen} = useContext(ChatContext);

	// Wrapper functions for transition setters
	const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
	const setTransitionOut = async (value) => {
		_setTransitionOut(value);
		if (value) await delay(250);
		return Promise.resolve();
	};
	const setRenderThanks = async () => {
		setTransitionOut(false);
		_setRenderThanks(true);
		await delay(1500);
		setTransitionOut(true).then(() => {
			_setRenderThanks(false);
		});
	};
	const setShowFeedback = (value) => {
		_setShowFeedback(value);
		if (isLastMessage) setIsLastFeedbackOpen(value);
	};

	const handleChange = (event, newState) => {
		// Make "Was this answer satisfying?" text disappear when user clicks "Yes" or "No"
		let initialTransitionOut = Promise.resolve();
		if (showText) {
			setTransitionButtons(true);
			initialTransitionOut = setTransitionOut(true);
			initialTransitionOut.then(() => {
				setShowText(false);
			});
		}

		// Show feedback form if user clicks "No" and hide it in any other case
		newState === 'dislike' ? setShowFeedback(true) : setShowFeedback(false);

		// Update state and send feedback if not already handled by WhatsWrong component
		if (newState !== 'done') {
			setState(newState);
			newState ? sendFeedback(messageId, newState, null, null) : sendFeedback(messageId, 'undislike', null, null);
		}

		// Thank user if feedback has been sent
		(newState === 'like' || newState === 'done') && initialTransitionOut.then(() => {
			setRenderThanks();
		});
	};

	// Hide text and close feedback form when new message sent
	useEffect(() => {
		if (!isLastMessage) setTransitionOut(true).then(() => {
			setShowText(false);
		});
		showFeedback ? handleChange('done') : null;
	}, [messages]);

	return (
		<div className={classNames(
			'feed-container',
			{'grey': isLastMessage,}
		)}>
			<div style={{display: 'flex', flexDirection: 'row'}}>
				<ToggleButtons state={state} showText={showText} hide={transitionButtons} handleChange={handleChange} />
				<p
					className={classNames(
						'paragraph',
						{'transition-out': transitionOut}
					)}
				>
					{showText ? t('feedback.sentences.wasSatisfying')
						: renderThanks ? t('feedback.sentences.thankYou')
							: null}
				</p>
			</div>
			<WhatsWrong showFeedback={showFeedback} messageId={messageId} handleFeedbackClick={handleChange} />
		</div>
	);
};

export default Feedback;
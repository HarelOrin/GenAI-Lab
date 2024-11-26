import React, { useContext, useRef, useEffect } from 'react';
import { ChatContext, ProductContext, SessionContext } from '../../../contexts';
import { useTranslation } from 'react-i18next';

import './History.css';
import assistantIcon from '../../../assets/assistantIcon.svg';
import { Spinner as NeSpinner } from '@nintexglobal/earthling-react';

import Message from './Message/Message';
import Badges from './Badges/Badges';
import Footer from './Footer/Footer';
import PromptExample from './PromptExample/PromptExample';

const History = () => {
	const { t } = useTranslation();
	const { messages, isWaiting, isLastFeedbackOpen } = useContext(ChatContext);
	const { generatingHistory } = useContext(SessionContext);
	const { searchQuery, product } = useContext(ProductContext);
	const formattedSearchQuery = searchQuery ? searchQuery.replace(/%20/g, ' ') : null;
	const historyContainerRef = useRef(null);

	// Auto scroll to the bottom
	useEffect(() => {
		const startTime = performance.now(); // Record the start time
		
		const scrollDuringTransition = (timestamp) => {
			const elapsed = timestamp - startTime;
		
			if (historyContainerRef.current) {
				if (isLastFeedbackOpen && elapsed < 300) {
					historyContainerRef.current.scrollTop = historyContainerRef.current.scrollHeight;
					requestAnimationFrame(scrollDuringTransition);
				} else {
					historyContainerRef.current.scrollTop = historyContainerRef.current.scrollHeight;
				}
			}
		};
		
		if (historyContainerRef.current) {
			if (isLastFeedbackOpen) {
				requestAnimationFrame(scrollDuringTransition);
			} else {
				historyContainerRef.current.scrollTop = historyContainerRef.current.scrollHeight;
			}
		}
	}, [messages, isWaiting, isLastFeedbackOpen, generatingHistory]);

	//=================================================================================================
	//                                       <History />
	//=================================================================================================
	return (
		<div className="history-container" ref={historyContainerRef}>
			<div className="history-center">
				<Badges />
				<div className="title-container" >
					<img src={assistantIcon} alt="Nintex Assistant" />
					<h1> {t('productName')} </h1>
					{!generatingHistory && <p>
						{t('history.description')}
					</p>}
				</div>
				{!generatingHistory ? (
					<div className="messages-container">
						{/* Conversation introduction */}
						<Message
							key={-1}
							message={{role:'assistant', content: t('history.messages.introductionMessage'), id: -1, sources: null}}
							isLastMessage={false}
							style={{marginBottom: 'auto'}}
						/>
						{/* Prompt exmaples */}
						{(!searchQuery && messages.length === 0 && product.id == 'docgen') && (
							<PromptExample />
						)}					
						{messages.map((message, index) => (
							<Message
								key={message.id}
								message={
									index === 0 && searchQuery
										? {
											id: message.id,
											role: message.role,
											content: t('history.messages.searchPrompt', { searchQuery: formattedSearchQuery }),
											sources: message.sources,
										}
										: message
								}
								isLastMessage={index === messages.length - 1}
								hideFeedback={false}
							/>
						))}

						{isWaiting && (
							<Message
								key={-2}
								message={{role:'assistant', content: t('history.loading.generatingMessage'), id: -2, sources: null}}
								isLastMessage={false}
								style={{marginBottom: 'auto'}}
							/>)}
					</div>
				) : (
					<NeSpinner status={t('history.loading.loadingConversation')} style={{ margin: 'auto' }}/>
				)}
				<Footer />
			</div>
		</div>
	);
};

export default History;

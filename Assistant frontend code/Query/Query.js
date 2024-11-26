import React, { useState, useContext, useRef, useEffect } from 'react';
import { ProductContext, ChatContext, SessionContext } from '../../../contexts';
import { useTranslation } from 'react-i18next';

import SendButton from './SendButton';

import './Query.css';

import { TextField } from '@mui/material';

const Query = () => {
	// Context & UI management
	const { t } = useTranslation();
	const { isWaiting, responseMode, sendMessage, messages, setMessages} = useContext(ChatContext);
	const { setCookie, getCookie, SESSION_ID_COOKIE } = useContext(SessionContext);
	const { product } = useContext(ProductContext);
	const [query, setQuery] = useState('');
	const inputRef = useRef(null);

	// Autofocus input after changes in isWaiting
	useEffect(() => {
		inputRef.current && inputRef.current.focus();
	}, [isWaiting]);

	// Functions
	const sendQuery = () => {
		// Check if the session cookie exists
		let storedSessionID = getCookie(SESSION_ID_COOKIE);

		setCookie(storedSessionID);

		if (inputRef.current) {
			inputRef.current.value = '';
		}

		setMessages((prevMessages) => [
			...prevMessages,
			{
				id: messages.length,
				role: 'user',
				content: query,
				sources: null,
			},
		]);

		sendMessage(query, product.id);
		setQuery('');
	};

	const handleQueryChange = (event) => {
		setQuery(event.target.value);
	};

	const handleKeyPress = (event) => {
		if (event.key === 'Enter' && !event.shiftKey && query.trim() !== '') {
			event.preventDefault();
			sendQuery();
		}
	};

	//====================================================================================================
	//                                            <Query />
	//====================================================================================================
	return (
		<div className="query-container">
			<div className="query-input">
				<TextField
					placeholder={t('query.askMeAnything', { productName: product.name })}
					sx={{
						backgroundColor: 'white',
						border: '1px solid #898F94',
						borderRadius: '4px',
					}}
					multiline
					fullWidth
					variant="outlined"
					rows={2}
					disabled={isWaiting || responseMode === 'sent'}
					inputRef={inputRef}
					value={query}
					onChange={handleQueryChange}
					onKeyPress={handleKeyPress}
					InputProps={{
						endAdornment: (
							<SendButton isDisabled={!query.trim() || isWaiting} sendQuery={sendQuery} />
						),
					}}
				/>
			</div>
		</div>
	);
};

export default Query;

"""
PyTorch Model Architecture Classes
Must match the training architecture exactly!
"""

import torch
import torch.nn as nn


class AttentionLayer(nn.Module):
    """Attention mechanism for BiLSTM"""
    def __init__(self, hidden_dim):
        super(AttentionLayer, self).__init__()
        self.attention = nn.Linear(hidden_dim, 1)
    
    def forward(self, lstm_output):
        # lstm_output shape: (batch, seq_len, hidden_dim)
        attention_weights = torch.softmax(self.attention(lstm_output), dim=1)
        # attention_weights shape: (batch, seq_len, 1)
        
        # Apply attention weights
        context = torch.sum(attention_weights * lstm_output, dim=1)
        # context shape: (batch, hidden_dim)
        
        return context, attention_weights


class ConfigurableBiLSTMAttentionModel(nn.Module):
    """
    Configurable BiLSTM with Attention for Genre Classification
    This is the model architecture used in training
    """
    def __init__(self, config, input_dim=58, num_classes=10):
        super(ConfigurableBiLSTMAttentionModel, self).__init__()
        
        self.config = config
        self.input_bn = nn.BatchNorm1d(1)
        
        # Layer 1
        self.lstm1 = nn.LSTM(
            input_dim, 
            config['lstm1_hidden_dim'], 
            batch_first=True, 
            bidirectional=config['bidirectional']
        )
        hidden1_output = config['lstm1_hidden_dim'] * (2 if config['bidirectional'] else 1)
        
        if config['use_attention']:
            self.attention1 = AttentionLayer(hidden1_output)
        self.bn1 = nn.BatchNorm1d(hidden1_output)
        self.dropout1 = nn.Dropout(config['dropout_lstm'])
        
        # Layer 2
        self.lstm2 = nn.LSTM(
            hidden1_output, 
            config['lstm2_hidden_dim'], 
            batch_first=True, 
            bidirectional=config['bidirectional']
        )
        hidden2_output = config['lstm2_hidden_dim'] * (2 if config['bidirectional'] else 1)
        
        if config['use_attention']:
            self.attention2 = AttentionLayer(hidden2_output)
        self.bn2 = nn.BatchNorm1d(hidden2_output)
        self.dropout2 = nn.Dropout(config['dropout_lstm'])
        
        # Layer 3
        self.lstm3 = nn.LSTM(
            hidden2_output, 
            config['lstm3_hidden_dim'], 
            batch_first=True, 
            bidirectional=config['bidirectional']
        )
        hidden3_output = config['lstm3_hidden_dim'] * (2 if config['bidirectional'] else 1)
        self.bn3 = nn.BatchNorm1d(hidden3_output)
        self.dropout3 = nn.Dropout(config['dropout_lstm'])
        
        # Dense layers
        self.fc1 = nn.Linear(hidden3_output, config['fc1_hidden_dim'])
        self.bn4 = nn.BatchNorm1d(config['fc1_hidden_dim'])
        self.dropout4 = nn.Dropout(config['dropout_fc'])
        
        self.fc2 = nn.Linear(config['fc1_hidden_dim'], config['fc2_hidden_dim'])
        self.bn5 = nn.BatchNorm1d(config['fc2_hidden_dim'])
        self.dropout5 = nn.Dropout(config['dropout_fc'])
        
        self.fc3 = nn.Linear(config['fc2_hidden_dim'], num_classes)
        
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.input_bn(x)
        
        # LSTM 1
        lstm1_out, _ = self.lstm1(x)
        if self.config['use_attention']:
            attn1_out, _ = self.attention1(lstm1_out)
            x = attn1_out
        else:
            x = lstm1_out[:, -1, :]
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout1(x)
        x = x.unsqueeze(1)
        
        # LSTM 2
        lstm2_out, _ = self.lstm2(x)
        if self.config['use_attention']:
            attn2_out, _ = self.attention2(lstm2_out)
            x = attn2_out
        else:
            x = lstm2_out[:, -1, :]
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout2(x)
        x = x.unsqueeze(1)
        
        # LSTM 3
        lstm3_out, _ = self.lstm3(x)
        x = lstm3_out[:, -1, :]
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout3(x)
        
        # Dense
        x = self.fc1(x)
        x = self.bn4(x)
        x = self.relu(x)
        x = self.dropout4(x)
        
        x = self.fc2(x)
        x = self.bn5(x)
        x = self.relu(x)
        x = self.dropout5(x)
        
        x = self.fc3(x)
        
        return x
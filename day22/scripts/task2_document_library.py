"""
Day 22 - Task 2: Document Library with FAISS.

Builds a library of 60 auto-generated documents across 6 topics,
chunks them with RecursiveCharacterTextSplitter (800 chars, 100
overlap), stores embeddings in FAISS with rich metadata, and
provides a search interface with metadata filtering.

Run from inside day22/scripts/ so outputs land in
day22/scripts/outputs/.

Toggle USE_OFFLINE=True (default) for sandbox / CI.
Set USE_OFFLINE=False on your machine with .venv312
to use the real MiniLM model.
"""

import json
import os
import time
import numpy as np


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
USE_OFFLINE = True   # Set False on .venv312 to use real HuggingFaceEmbeddings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


# ---------------------------------------------------------------------------
# Embedder helpers (same pattern as Task 1 & Day 21)
# ---------------------------------------------------------------------------

def get_embedder():
    """Return the appropriate embedder based on USE_OFFLINE flag."""
    if USE_OFFLINE:
        return OfflineEmbedder()
    from langchain_huggingface import HuggingFaceEmbeddings  # noqa: PLC0415
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


class OfflineEmbedder:
    """Deterministic 384-dim embedder for offline/sandbox testing."""

    DIM = 384

    def embed_documents(self, texts):
        """Embed a list of texts deterministically."""
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        """Embed a single query text deterministically."""
        return self._embed(text)

    def _embed(self, text):
        """Hash-seed RNG so same text → same vector every run."""
        seed = sum(ord(c) for c in text) % (2 ** 31)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(self.DIM).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()


# ---------------------------------------------------------------------------
# Auto-generated document corpus (60 documents across 6 topics)
# ---------------------------------------------------------------------------

def build_corpus():
    """Return list of (title, body, source, section) tuples."""
    corpus = []

    # --- Machine Learning (10 docs) ---
    ml_docs = [
        ("Supervised Learning Basics",
         "Supervised learning trains a model on labelled examples. Each "
         "training sample has an input feature vector and a ground-truth "
         "output label. The model learns a mapping function f(x)→y by "
         "minimising a loss function such as mean-squared error for "
         "regression or cross-entropy for classification. Common algorithms "
         "include linear regression, logistic regression, decision trees, "
         "random forests, gradient boosting, and support vector machines. "
         "The key challenge is generalisation: the model must perform well "
         "on unseen data, not just the training set. Techniques like "
         "cross-validation, regularisation (L1/L2), and early stopping help "
         "prevent overfitting. Evaluation metrics vary by task: accuracy, "
         "precision, recall, F1-score for classification; RMSE, MAE, R² "
         "for regression."),
        ("Unsupervised Learning Overview",
         "Unsupervised learning discovers hidden structure in unlabelled "
         "data. Without predefined labels the algorithm must infer patterns "
         "on its own. Clustering groups similar data points: k-means "
         "partitions data into k centroids; hierarchical clustering builds "
         "a dendrogram; DBSCAN finds density-based clusters of arbitrary "
         "shape. Dimensionality reduction compresses high-dimensional data: "
         "PCA finds orthogonal directions of maximum variance; t-SNE "
         "preserves local neighbourhoods for 2D/3D visualisation; UMAP "
         "scales better than t-SNE for large datasets. Autoencoders learn "
         "compact latent representations through an encoder-decoder "
         "architecture. Association rule mining finds co-occurring item "
         "sets in transaction data using metrics like support, confidence, "
         "and lift."),
        ("Gradient Descent Optimisation",
         "Gradient descent minimises a loss function by iteratively moving "
         "parameters in the direction of steepest descent (negative "
         "gradient). Batch gradient descent computes the gradient over the "
         "entire dataset — accurate but slow. Stochastic gradient descent "
         "(SGD) uses one sample per update — fast but noisy. Mini-batch "
         "SGD balances both by using small batches (32–256 samples). "
         "Adaptive optimisers adjust learning rates per-parameter: AdaGrad "
         "accumulates squared gradients; RMSProp adds exponential decay; "
         "Adam combines momentum and RMSProp. Learning rate scheduling "
         "(step decay, cosine annealing, warm restarts) further improves "
         "convergence. Gradient clipping prevents exploding gradients in "
         "deep or recurrent networks."),
        ("Overfitting and Regularisation",
         "Overfitting occurs when a model memorises training data instead "
         "of learning general patterns, leading to poor performance on new "
         "data. The bias-variance tradeoff explains this: high-complexity "
         "models have low bias but high variance. L1 regularisation (Lasso) "
         "adds the absolute sum of weights to the loss, encouraging sparse "
         "solutions. L2 regularisation (Ridge) adds the squared sum, "
         "shrinking weights smoothly. Dropout randomly disables neurons "
         "during training, acting as an ensemble of subnetworks. Data "
         "augmentation artificially increases training data. Early stopping "
         "halts training when validation loss starts rising. Batch "
         "normalisation reduces internal covariate shift and acts as mild "
         "regularisation."),
        ("Ensemble Methods",
         "Ensemble methods combine multiple models to produce superior "
         "predictions. Bagging (bootstrap aggregating) trains models on "
         "random data subsets and averages predictions; Random Forest is "
         "the canonical example. Boosting trains models sequentially, each "
         "correcting the errors of the previous: AdaBoost reweights "
         "misclassified samples; Gradient Boosting fits residuals; XGBoost "
         "and LightGBM add regularisation and histogram-based splits for "
         "speed. Stacking (stacked generalisation) uses a meta-learner to "
         "combine base model predictions. Voting classifiers use majority "
         "vote (hard) or averaged probabilities (soft). Ensembles almost "
         "always outperform single models in competitions but are slower "
         "to train and harder to interpret."),
        ("Feature Engineering",
         "Feature engineering transforms raw data into informative inputs "
         "for machine learning models. Numerical features benefit from "
         "scaling (standardisation, min-max normalisation) and "
         "transformation (log, sqrt for skewed distributions). Categorical "
         "features are encoded via one-hot, ordinal, or target encoding. "
         "Date-time features yield cyclic encodings (sin/cos) or derived "
         "fields (day-of-week, quarter). Text features use TF-IDF, "
         "bag-of-words, or learned embeddings. Interaction features capture "
         "non-linear relationships between pairs of variables. Polynomial "
         "features expand the feature space. Feature selection reduces "
         "dimensionality via filter methods (correlation, mutual "
         "information), wrapper methods (recursive feature elimination), "
         "or embedded methods (LASSO coefficients)."),
        ("Model Evaluation Metrics",
         "Choosing the right evaluation metric is critical. For "
         "classification: accuracy is misleading on imbalanced datasets; "
         "precision measures positive prediction quality;"
         " recall (sensitivity) "
         "measures coverage of actual positives; F1-score is their harmonic "
         "mean. The ROC curve plots TPR vs FPR; AUC-ROC measures overall "
         "discriminative ability. For regression: MAE is robust to outliers; "
         "RMSE penalises large errors more; R² measures explained variance. "
         "For ranking: NDCG, MAP, MRR. For clustering: silhouette score, "
         "Davies-Bouldin index. Cross-validation provides more reliable "
         "estimates than a single train/test split, especially on small "
         "datasets."),
        ("Transfer Learning",
         "Transfer learning leverages knowledge from a pre-trained model "
         "for a new task, dramatically reducing the need for labelled data "
         "and training time. A backbone network (e.g. ResNet, BERT) is "
         "pre-trained on a large dataset, then fine-tuned on the target "
         "task. Feature extraction freezes the backbone and trains only a "
         "new classification head. Fine-tuning unfreezes some or all layers "
         "for joint training. Domain adaptation handles distribution shift "
         "between source and target datasets. Few-shot learning adapts with "
         "very few examples. Prompt tuning and LoRA are parameter-efficient "
         "fine-tuning methods for large language models that avoid "
         "retraining all weights."),
        ("Cross-Validation Strategies",
         "Cross-validation estimates model generalisation by partitioning "
         "data into training and validation folds. K-fold CV splits data "
         "into k equal parts, trains on k-1, validates on 1, rotates k "
         "times, and averages metrics. Stratified k-fold preserves class "
         "proportions in each fold — essential for imbalanced datasets. "
         "Leave-one-out CV (LOOCV) uses n-1 samples for training — "
         "expensive but unbiased. Time-series CV uses expanding or rolling "
         "windows to prevent data leakage. Group k-fold prevents samples "
         "from the same group appearing in both train and validation sets. "
         "Nested CV separates hyperparameter tuning from model evaluation "
         "for an unbiased performance estimate."),
        ("Hyperparameter Tuning",
         "Hyperparameters control the learning process and model capacity; "
         "they are set before training, unlike parameters learned from "
         "data. Grid search exhaustively tries all combinations in a "
         "specified grid — thorough but exponentially expensive. Random "
         "search samples combinations at random, often finding good "
         "solutions faster. Bayesian optimisation builds a probabilistic "
         "model of the objective function to guide search toward promising "
         "regions. Successive halving and Hyperband allocate compute "
         "budget adaptively, discarding poor configurations early. "
         "AutoML frameworks (Optuna, Ray Tune, FLAML) automate this "
         "process. Early stopping in neural network tuning prevents "
         "wasted compute on clearly bad hyperparameter sets."),
    ]

    # --- Deep Learning (10 docs) ---
    dl_docs = [
        ("Convolutional Neural Networks",
         "CNNs use convolutional layers to learn spatial hierarchies of "
         "features from grid-structured data like images. A convolution "
         "applies a small learnable filter across the input, sharing weights "
         "spatially to achieve translation invariance. Pooling layers "
         "(max-pool, average-pool) downsample feature maps, reducing "
         "spatial dimensions and computation. Batch normalisation stabilises "
         "activations. Residual connections (ResNet) allow gradients to "
         "flow directly through skip connections, enabling very deep "
         "networks. Modern architectures include"
         " VGG, Inception, EfficientNet, "
         "and Vision Transformers (ViT) which treat image patches as tokens "
         "for self-attention. CNNs dominate image classification, object "
         "detection, and semantic segmentation tasks."),
        ("Recurrent Neural Networks",
         "RNNs process sequential data by maintaining a hidden state "
         "updated at each timestep. The vanishing gradient problem makes "
         "plain RNNs struggle with long-range dependencies. LSTMs add "
         "cell state and gates (input, forget, output) that control "
         "information flow, learning to retain or discard context over "
         "hundreds of steps. GRUs simplify LSTMs with reset and update "
         "gates, using fewer parameters with similar performance. "
         "Bidirectional RNNs process sequences in both directions, "
         "capturing past and future context. Sequence-to-sequence models "
         "with attention (the precursor to Transformers) power early "
         "neural machine translation systems."),
        ("Transformer Architecture",
         "Transformers replaced RNNs for sequence modelling by relying "
         "entirely on self-attention. The self-attention mechanism computes "
         "query, key, value projections and attends to all positions "
         "simultaneously in O(n²) time. Multi-head attention runs several "
         "attention heads in parallel, each attending to different "
         "representation subspaces. Positional encodings inject order "
         "information since attention is permutation-invariant. The "
         "encoder-decoder structure suits seq2seq tasks; encoder-only "
         "models (BERT) excel at understanding; decoder-only models "
         "(GPT) excel at generation. Efficient variants (Longformer, "
         "FlashAttention) reduce the quadratic complexity for long "
         "sequences."),
        ("Attention Mechanisms",
         "Attention allows models to focus on relevant parts of the input "
         "when producing each output. Bahdanau (additive) attention "
         "introduced soft alignment between encoder hidden states and the "
         "decoder. Luong (multiplicative) attention uses dot-product "
         "scoring, more efficient. Scaled dot-product attention divides "
         "by the square root of the key dimension to prevent softmax "
         "saturation. Cross-attention in Transformers attends across two "
         "sequences (encoder output and decoder state). Self-attention "
         "attends within a single sequence. Flash Attention recomputes "
         "attention in tiles to avoid storing the full n×n matrix in GPU "
         "memory, enabling much longer context windows."),
        ("Generative Adversarial Networks",
         "GANs consist of a generator that creates synthetic data and a "
         "discriminator that distinguishes real from fake. Trained "
         "adversarially, the generator learns to fool the discriminator. "
         "Mode collapse (the generator produces limited diversity) and "
         "training instability are key challenges. Progressive GAN grows "
         "the network resolution gradually. StyleGAN2 achieves "
         "photorealistic face synthesis by separating content and style. "
         "Conditional GANs add class labels or image prompts to guide "
         "generation. Pix2Pix performs paired image-to-image translation. "
         "CycleGAN enables unpaired image translation using cycle "
         "consistency loss. Diffusion models have largely superseded GANs "
         "for image generation due to better stability and diversity."),
        ("Variational Autoencoders",
         "VAEs learn a probabilistic latent space by encoding inputs to "
         "distributions (mean and variance) rather than point vectors. "
         "The reparameterisation trick makes sampling differentiable: "
         "z = μ + σ·ε where ε ~ N(0,1). The loss combines reconstruction "
         "loss with KL divergence, which regularises the latent space to "
         "be approximately Gaussian. VAEs enable smooth interpolation "
         "between data points and controlled generation by sampling or "
         "manipulating the latent vector. Conditional VAEs condition "
         "generation on class labels. VAE-GAN hybrids combine sharp "
         "GAN outputs with the structured latent space of VAEs. VQ-VAEs "
         "use discrete latent codes, forming the backbone of image "
         "tokenisation in models like DALL-E."),
        ("Diffusion Models",
         "Diffusion models generate data by learning to reverse a gradual "
         "noising process. The forward process adds Gaussian noise over T "
         "timesteps until the signal is pure noise. A neural network "
         "(usually a U-Net) learns to predict and remove noise at each "
         "step. DDPM (Denoising Diffusion Probabilistic Models) proved "
         "diffusion could match GANs in image quality with better "
         "diversity. DDIM enables faster sampling with fewer steps. "
         "Classifier-free guidance steers generation toward a condition "
         "(text prompt, class) without a separate classifier. Stable "
         "Diffusion runs diffusion in the latent space of a VAE, "
         "dramatically reducing compute. Diffusion models now dominate "
         "image, audio, and video generation benchmarks."),
        ("Loss Functions in Deep Learning",
         "The loss function measures the discrepancy between predictions "
         "and targets and drives parameter updates. Cross-entropy loss "
         "is standard for classification: binary cross-entropy for two "
         "classes; categorical cross-entropy for multiclass with softmax. "
         "Mean squared error (MSE) is the default for regression; mean "
         "absolute error (MAE) is more robust to outliers; Huber loss "
         "combines both. Contrastive loss and triplet loss pull similar "
         "pairs closer and push dissimilar pairs apart in embedding space. "
         "InfoNCE loss underpins self-supervised contrastive learning "
         "(SimCLR, MoCo). Focal loss downweights easy negatives to focus "
         "training on hard examples — useful for object detection on "
         "imbalanced foreground/background."),
        ("Batch Normalisation and Layer Normalisation",
         "Normalisation layers stabilise training by reducing internal "
         "covariate shift. Batch normalisation computes mean and variance "
         "over the batch dimension and normalises, then applies learnable "
         "scale (γ) and shift (β). It accelerates training and allows "
         "higher learning rates but behaves differently at inference "
         "(uses running statistics). Layer normalisation computes "
         "statistics over the feature dimension per sample, making it "
         "batch-size independent — preferred in Transformers and RNNs. "
         "Group normalisation divides channels into groups, good for "
         "small-batch settings like object detection. Instance "
         "normalisation normalises each channel per sample, used in "
         "style transfer. Root mean square normalisation (RMSNorm) "
         "omits the mean-centering step for efficiency."),
        ("Neural Architecture Search",
         "Neural Architecture Search (NAS) automates the design of neural "
         "network architectures. Reinforcement learning-based NAS trains "
         "a controller RNN to generate architectures and uses validation "
         "accuracy as a reward — pioneered by Google Brain but extremely "
         "expensive. Evolutionary NAS mutates and selects architectures "
         "over generations. Differentiable NAS (DARTS) relaxes the "
         "discrete architecture search to a continuous optimisation "
         "problem, enabling gradient-based search. One-shot NAS trains "
         "a supernet that shares weights across all candidate "
         "sub-architectures. EfficientNet, found by NAS, uses compound "
         "scaling to jointly scale depth, width, and resolution. NAS is "
         "increasingly used to design efficient models for edge devices."),
    ]

    # --- NLP (10 docs) ---
    nlp_docs = [
        ("Word Embeddings",
         "Word embeddings represent words as dense vectors in a continuous "
         "space where semantic similarity correlates with geometric "
         "proximity. Word2Vec (2013) introduced two architectures: CBOW "
         "predicts a word from context; Skip-gram predicts context from "
         "a word. GloVe trains on global word co-occurrence statistics. "
         "FastText extends Word2Vec to subword n-grams, handling "
         "out-of-vocabulary words. ELMo provides contextualised embeddings "
         "from a bidirectional LSTM, giving different representations for "
         "polysemous words. Modern contextual embeddings from BERT and "
         "GPT have replaced static embeddings for downstream tasks. "
         "Sentence embeddings (Sentence-BERT, all-MiniLM-L6-v2) extend "
         "this to full sentences for semantic similarity."),
        ("BERT and Pre-trained Language Models",
         "BERT (Bidirectional Encoder Representations from Transformers) "
         "pre-trains a Transformer encoder using masked language modelling "
         "(predict randomly masked tokens) and next-sentence prediction. "
         "Pre-training on large corpora (Wikipedia + BookCorpus) captures "
         "rich linguistic knowledge. Fine-tuning adds a task-specific "
         "head and trains end-to-end on labelled data, achieving "
         "state-of-the-art on 11 NLP tasks at release. RoBERTa removes "
         "next-sentence prediction and trains longer with larger batches. "
         "ALBERT uses parameter sharing across layers for efficiency. "
         "DistilBERT knowledge-distills BERT to 60% size with 97% "
         "performance. DeBERTa adds disentangled attention and virtual "
         "adversarial training for further gains."),
        ("Named Entity Recognition",
         "Named entity recognition (NER) identifies and classifies "
         "entities in text (person, organisation, location, date, "
         "quantity). Early systems used hand-crafted rules and gazetteers. "
         "Statistical models (CRF, HMM) treat NER as sequence labelling "
         "with BIO/BIOES tagging schemes. BiLSTM-CRF combines "
         "bidirectional LSTMs for context and a CRF for globally "
         "consistent label sequences. BERT fine-tuned for token "
         "classification achieves near-human performance on CoNLL-2003. "
         "Span-based NER models predict start/end positions and entity "
         "type jointly, handling nested entities. Zero-shot NER uses "
         "LLMs to identify entity types without task-specific training."),
        ("Text Classification",
         "Text classification assigns predefined categories to text. "
         "Traditional approaches use TF-IDF features with Naive Bayes, "
         "SVM, or logistic regression. FastText trains a shallow network "
         "on n-gram features very quickly, competitive with deep models "
         "on many tasks. CNN for text slides filters over word embeddings "
         "to capture local n-gram patterns. Hierarchical attention "
         "networks model both word and sentence importance. Fine-tuned "
         "BERT sets the standard for accuracy. Few-shot classification "
         "with GPT-3/4 uses in-context examples. Multi-label "
         "classification assigns multiple tags per document (topics, "
         "emotions). Prompt-based classification rephrases tasks as text "
         "generation, leveraging LLMs without fine-tuning."),
        ("Machine Translation",
         "Machine translation automatically converts text from one "
         "language to another. Rule-based MT uses hand-crafted linguistic "
         "rules — high precision but limited coverage. Statistical MT "
         "learns phrase translation tables from parallel corpora. Neural "
         "MT (seq2seq with attention) drastically improved fluency. "
         "Transformers (Google's original paper) set the current standard: "
         "multi-head attention captures long-range dependencies without "
         "sequential processing. Back-translation augments training data "
         "by translating target-side monolingual text. Multilingual "
         "models (mBART, mT5, NLLB) translate between 200+ language "
         "pairs with a single model. Quality is measured by BLEU score, "
         "though human evaluation remains necessary for nuance."),
        ("Sentiment Analysis",
         "Sentiment analysis determines the emotional tone of text — "
         "typically positive, negative, or neutral. Lexicon-based methods "
         "use sentiment dictionaries (VADER, AFINN, SentiWordNet). "
         "Machine learning approaches train classifiers on labelled "
         "reviews (IMDb, Amazon). Aspect-based sentiment analysis (ABSA) "
         "identifies sentiment toward specific aspects (food quality, "
         "service, price). Transformer fine-tuning achieves high accuracy "
         "on benchmark datasets. Challenges include sarcasm, negation, "
         "domain shift, and cross-lingual sentiment. Multimodal sentiment "
         "analysis combines text, audio, and video signals. Applications "
         "span social media monitoring, brand management, financial "
         "signal extraction, and customer feedback analysis."),
        ("Question Answering Systems",
         "Question answering systems retrieve or generate answers from "
         "text. Extractive QA identifies answer spans in a context "
         "passage: BERT fine-tuned on SQuAD predicts start and end "
         "token positions. Retrieval-augmented generation (RAG) first "
         "retrieves relevant documents then generates the answer with an "
         "LLM. Open-domain QA searches a large corpus (Wikipedia) for "
         "relevant passages. Knowledge base QA queries structured "
         "databases via SPARQL or entity linking. Multi-hop QA requires "
         "reasoning over multiple documents to answer complex questions. "
         "Reading comprehension benchmarks include SQuAD, TriviaQA, "
         "NaturalQuestions, and HotpotQA. LLMs now handle conversational "
         "QA with follow-up questions and clarifications."),
        ("Text Summarisation",
         "Text summarisation condenses documents while preserving key "
         "information. Extractive methods select and concatenate salient "
         "sentences using graph algorithms (TextRank), neural sentence "
         "scoring, or clustering. Abstractive methods generate new text "
         "using seq2seq models. PEGASUS pre-trains on gap-sentence "
         "generation (masking key sentences) as a summarisation-specific "
         "pre-training objective. BART uses a denoising autoencoder "
         "pre-training scheme and excels at generation tasks including "
         "summarisation. T5 casts all NLP tasks as text-to-text, "
         "achieving strong summarisation results. Factuality remains a "
         "challenge: models sometimes hallucinate facts not in the "
         "source. Evaluation uses ROUGE scores comparing n-gram overlap "
         "with reference summaries."),
        ("Information Retrieval",
         "Information retrieval (IR) finds relevant documents for a "
         "query. Classical IR relies on term frequency statistics: TF-IDF "
         "ranks documents by weighted term importance; BM25 adds document "
         "length normalisation and is still a strong baseline. Inverted "
         "indexes enable fast keyword lookup at web scale. Dense retrieval "
         "encodes queries and documents into vectors and uses approximate "
         "nearest-neighbour search (FAISS, ScaNN). Bi-encoder models "
         "(DPR, E5, BGE) encode query and document independently. "
         "Cross-encoder re-rankers attend jointly over query-document "
         "pairs for higher precision but lower speed. Hybrid retrieval "
         "combines sparse BM25 with dense embeddings. ColBERT uses "
         "late interaction (MaxSim over token embeddings) for accuracy "
         "between the two approaches."),
        ("Large Language Models",
         "Large language models (LLMs) are Transformer-based models "
         "trained on trillions of tokens via next-token prediction. "
         "Scaling laws show loss decreases predictably with compute, "
         "data, and parameters. GPT-3 demonstrated emergent few-shot "
         "capabilities at 175B parameters. Instruction tuning (FLAN, "
         "InstructGPT) fine-tunes LLMs to follow natural language "
         "instructions. RLHF (reinforcement learning from human feedback) "
         "aligns model outputs with human preferences, used in ChatGPT. "
         "Constitutional AI (Anthropic) trains models to be helpful, "
         "harmless, and honest. Open-weight LLMs (LLaMA, Mistral, "
         "Qwen) enable local deployment. Quantisation (GGUF, AWQ, GPTQ) "
         "reduces memory footprint for inference on consumer hardware."),
    ]

    # --- Vector Databases (10 docs) ---
    vdb_docs = [
        ("Introduction to Vector Databases",
         "Vector databases are purpose-built systems for storing and "
         "querying high-dimensional embedding vectors. Unlike traditional "
         "databases that match exact values, vector databases retrieve "
         "semantically similar items using approximate nearest-neighbour "
         "(ANN) algorithms. They are the backbone of modern semantic "
         "search, recommendation engines, and retrieval-augmented "
         "generation (RAG) pipelines. Key features include: fast ANN "
         "indexing (HNSW, IVF, PQ), metadata filtering, hybrid search "
         "(dense + sparse), real-time upsert, and horizontal scalability. "
         "Popular systems include Pinecone, Weaviate, Qdrant, Milvus, "
         "Chroma, and LanceDB. FAISS is a library (not a full database) "
         "but is widely used for in-process vector search."),
        ("FAISS Deep Dive",
         "FAISS (Facebook AI Similarity Search) is a C++ library with "
         "Python bindings for efficient similarity search. IndexFlatL2 "
         "performs exact brute-force L2 search — accurate but O(n) per "
         "query. IndexFlatIP uses inner product; with normalised vectors "
         "this equals cosine similarity. IndexIVFFlat partitions vectors "
         "into Voronoi cells using k-means; search probes nprobe nearest "
         "cells, trading recall for speed. Product quantisation (PQ) "
         "compresses vectors by encoding sub-vectors independently, "
         "reducing memory dramatically. IndexHNSW builds a hierarchical "
         "navigable small-world graph; search traverses the graph "
         "greedily. GPU indices move computation to CUDA for orders-of-"
         "magnitude speedup. FAISS supports batch operations and "
         "ID-mapped indexes for delete/update via IDMap wrappers."),
        ("Chroma Vector Database",
         "Chroma is an open-source vector database designed for LLM "
         "applications. It supports persistent storage (DuckDB + Parquet "
         "on disk or SQLite) and in-memory mode. Collections store "
         "documents, embeddings, and rich metadata together. The Python "
         "client provides a simple API: add(), query(), delete(), get(), "
         "update(). Chroma integrates natively with LangChain, LlamaIndex, "
         "and Haystack. Metadata filtering uses a MongoDB-style query "
         "language with operators like $eq, $in, $gte. Chroma uses HNSW "
         "(via hnswlib) for fast ANN search. It is well-suited for "
         "prototyping and small-to-medium datasets. Chroma Cloud offers "
         "a hosted version with authentication and multi-tenant support."),
        ("HNSW Algorithm",
         "Hierarchical Navigable Small World (HNSW) is the leading ANN "
         "algorithm for high recall at low latency. It builds a "
         "multi-layer graph where upper layers have long-range edges "
         "(coarse navigation) and lower layers have short-range edges "
         "(fine-grained search). Insertion places a new node at a random "
         "maximum layer, connects it to the ef_construction nearest "
         "neighbours at each layer via greedy beam search. Query starts "
         "at the top layer entry point, greedily descends to layer 0, "
         "then returns the ef nearest neighbours from a priority queue. "
         "Parameters M (connections per node) and ef_construction control "
         "the index-quality tradeoff. HNSW achieves >99% recall at "
         "millisecond latency on million-scale datasets."),
        ("Product Quantisation",
         "Product quantisation (PQ) compresses high-dimensional vectors "
         "to drastically reduce memory. The vector is split into m "
         "sub-vectors of equal dimension d/m. Each sub-space is "
         "independently quantised using a codebook of k* centroids "
         "trained by k-means. A vector is then represented by m centroid "
         "indices (m bytes if k*=256), reducing 384×4=1536 bytes per "
         "float32 vector to just m bytes. Distance approximation is "
         "computed via asymmetric distance computation (ADC) using "
         "pre-computed sub-distance tables. PQ is combined with IVF in "
         "IndexIVFPQ for billion-scale search. Scalar quantisation (SQ) "
         "is a simpler alternative that quantises each dimension "
         "independently. Both are crucial for web-scale retrieval."),
        ("Pinecone Managed Vector Database",
         "Pinecone is a fully managed, cloud-native vector database. "
         "It abstracts all infrastructure: no index tuning, no server "
         "management, and automatic scaling. Namespaces logically "
         "partition vectors within an index. Metadata filters apply "
         "server-side before or after ANN search. Pinecone supports "
         "sparse-dense hybrid search combining BM25 keyword scores "
         "with dense embedding scores. Serverless indexes charge per "
         "query and storage rather than provisioned replicas. "
         "Pod-based indexes offer dedicated compute with predictable "
         "latency. The Python client wraps REST calls. Pinecone is "
         "GDPR-compliant and SOC 2 certified. It integrates with "
         "LangChain, LlamaIndex, and major embedding providers."),
        ("Weaviate Vector Database",
         "Weaviate is an open-source vector database with a GraphQL "
         "API and modular vectoriser ecosystem. It stores objects in "
         "a schema with classes and properties, auto-vectorising text "
         "with pluggable modules (OpenAI, Cohere, HuggingFace). HNSW "
         "is the default index; flat BQ index added for small datasets. "
         "Hybrid search combines BM25 keyword scores with vector "
         "similarity via a fusion algorithm. Multi-tenancy isolates "
         "tenant data in separate HNSW shards. Weaviate Cloud (WCS) "
         "offers managed hosting. References between objects model "
         "relationships like a graph. The Python v4 client uses "
         "collections instead of classes. Generative search modules "
         "pipe retrieved results directly into LLM prompts for RAG."),
        ("Qdrant Vector Search Engine",
         "Qdrant is a Rust-based vector search engine with a focus on "
         "performance and filtering. It stores named collections of "
         "points, each with a vector, payload (metadata), and integer "
         "or UUID id. HNSW is the core index with quantisation support "
         "(scalar, product, binary). Payload filtering applies indexed "
         "field conditions during ANN search, achieving near-exact "
         "recall even with complex filters via HNSW graph filtering. "
         "Sparse vectors for keyword search are supported natively. "
         "Qdrant supports multi-vector points (dense + sparse + "
         "colbert-style). gRPC and REST APIs, Docker-friendly. "
         "Qdrant Cloud offers managed deployment. The Python SDK "
         "provides a high-level client with full type hints."),
        ("Milvus Distributed Vector Database",
         "Milvus is a cloud-native, distributed vector database "
         "designed for billion-scale datasets. It separates compute "
         "and storage: query nodes handle search, data nodes handle "
         "ingestion, index nodes build indexes asynchronously. "
         "Supported indexes include HNSW, IVF_FLAT, IVF_SQ8, "
         "IVF_PQ, DISKANN, and GPU indexes. Milvus 2.x uses a "
         "message queue (Pulsar/Kafka) for streaming ingestion. "
         "Collections have multiple vector fields and scalar fields "
         "for metadata. Partitions and partition keys enable data "
         "isolation. Pymilvus is the Python SDK. Milvus Lite is an "
         "embedded version for prototyping. Zilliz Cloud is the "
         "managed offering. Milvus handles multi-vector retrieval "
         "and reranking natively."),
        ("Embedding Models for Retrieval",
         "Embedding models project text into vectors that capture "
         "semantic meaning. Bi-encoder models like all-MiniLM-L6-v2, "
         "all-mpnet-base-v2, and E5-large-v2 encode query and "
         "document independently — essential for retrieval speed. "
         "The MTEB benchmark evaluates models across retrieval, "
         "classification, clustering, and STS tasks. BGE-m3 is a "
         "multilingual model supporting dense, sparse, and colbert "
         "retrieval with a single encoder. OpenAI text-embedding-3-"
         "large achieves top MTEB scores but requires an API. "
         "Matryoshka embeddings (MRL) train models that produce "
         "accurate embeddings at multiple truncated dimensions, "
         "enabling compute-quality tradeoffs. Late interaction "
         "models (ColBERT) store per-token embeddings for MaxSim "
         "scoring."),
    ]

    # --- RAG (10 docs) ---
    rag_docs = [
        ("RAG Architecture Overview",
         "Retrieval-Augmented Generation (RAG) enhances LLM responses "
         "by grounding them in retrieved external knowledge. The "
         "pipeline has three stages: indexing, retrieval, and "
         "generation. Indexing loads and chunks documents, embeds "
         "chunks with a bi-encoder, and stores them in a vector store. "
         "Retrieval encodes the query and finds the top-k similar "
         "chunks via ANN search. Generation feeds retrieved chunks "
         "as context to an LLM, which synthesises a grounded answer. "
         "RAG reduces hallucination, enables knowledge updates without "
         "retraining, and supports source citation. Naive RAG uses "
         "simple retrieval; Advanced RAG adds query rewriting, "
         "hypothetical document embeddings (HyDE), and re-ranking; "
         "Modular RAG assembles custom pipelines with interchangeable "
         "components."),
        ("Chunking Strategies for RAG",
         "Chunking splits documents into pieces small enough to fit "
         "in an LLM's context window but large enough to be "
         "semantically coherent. Fixed-size chunking splits by "
         "character count — fast but may cut sentences. Recursive "
         "splitting tries paragraph, sentence, then character "
         "boundaries in order — better at natural boundaries. "
         "Sentence-window chunking stores small sentence chunks for "
         "retrieval but expands to surrounding sentences as context "
         "at generation time. Semantic chunking groups sentences "
         "that are semantically similar using embedding similarity. "
         "Chunk overlap prevents information loss at boundaries. "
         "The optimal chunk size depends on the embedding model's "
         "input limit and the LLM's context window. Day 18 findings: "
         "chunks of 400 chars with 60 overlap gave the best "
         "retrieval-to-coherence tradeoff."),
        ("Hybrid Search in RAG",
         "Hybrid search combines dense vector retrieval with sparse "
         "keyword search (BM25) for better coverage. Dense retrieval "
         "excels at semantic matching ('heart attack' ↔ 'myocardial "
         "infarction') but may miss exact keyword matches. Sparse "
         "BM25 excels at rare keyword and entity matching but ignores "
         "semantics. Reciprocal rank fusion (RRF) merges ranked lists "
         "from both systems without requiring score normalisation. "
         "Weaviate and Qdrant support hybrid search natively. "
         "LangChain's EnsembleRetriever combines any two retrievers "
         "with configurable weights. Hybrid typically outperforms "
         "either component alone on diverse real-world query sets. "
         "The optimal dense-to-sparse weight ratio varies by domain "
         "and should be tuned on a held-out evaluation set."),
        ("Re-ranking in RAG",
         "Re-ranking applies a more powerful but slower model to "
         "re-score the initial retrieval set, improving precision. "
         "Cross-encoder re-rankers (Cohere Rerank, BGE-reranker, "
         "ms-marco-MiniLM) attend jointly over query and document, "
         "capturing fine-grained interactions missed by bi-encoders. "
         "LLM-based re-ranking uses the LLM itself to score "
         "relevance, leveraging its reasoning ability. RankGPT "
         "prompts GPT-4 with a listwise ranking instruction. The "
         "typical pipeline: retrieve top-50 with dense ANN, rerank "
         "to top-5, pass to LLM. UPR (unsupervised passage reranking) "
         "uses the generative likelihood of the query given the "
         "passage. Re-ranking adds latency but significantly improves "
         "answer quality, especially for multi-hop questions."),
        ("Query Transformation Techniques",
         "Query transformation improves retrieval by rewriting or "
         "expanding the user query before embedding. HyDE "
         "(Hypothetical Document Embeddings) prompts an LLM to "
         "generate a hypothetical answer to the query, then embeds "
         "that answer — pulling retrieval toward document-space. "
         "Multi-query retrieval generates N paraphrases of the "
         "query, retrieves for each, and deduplicates results. "
         "Step-back prompting abstracts the query to a higher-level "
         "concept before retrieval. Query decomposition splits "
         "complex questions into sub-questions answered in parallel "
         "or sequentially. Contextual compression distils retrieved "
         "chunks down to only the relevant sentences before passing "
         "to the LLM. These techniques address vocabulary mismatch, "
         "vague queries, and under-specified questions."),
        ("Evaluation of RAG Systems",
         "Evaluating RAG requires assessing both retrieval and "
         "generation quality. Retrieval metrics: Recall@K (fraction "
         "of relevant documents in top-K), Precision@K, MRR (mean "
         "reciprocal rank), NDCG. Generation metrics: ROUGE, BLEU, "
         "BERTScore for reference-based evaluation; faithfulness, "
         "answer relevance, and context precision for reference-free "
         "evaluation using an LLM-as-judge. RAGAS is an open-source "
         "framework that automates these LLM-as-judge metrics. "
         "TruLens evaluates RAG with the RAG triad: context relevance, "
         "groundedness, and answer relevance. Human evaluation "
         "remains the gold standard but is expensive and slow. "
         "End-to-end benchmarks like BEIR, KILT, and RGB test RAG "
         "pipelines on diverse open-domain tasks."),
        ("Long Context vs RAG",
         "LLMs now support context windows of 128K-1M tokens, "
         "raising the question: why chunk and retrieve when you can "
         "feed everything at once? RAG remains preferable when: the "
         "corpus is larger than any context window (millions of "
         "documents); latency constraints preclude long-context "
         "inference; privacy requires only relevant chunks to be "
         "sent to a hosted API; source attribution is required. "
         "Long-context models struggle with the 'lost in the middle' "
         "phenomenon: attention degrades for content far from the "
         "query in the middle of a long prompt. RAG + long-context "
         "is a winning combination: retrieve a coarse set, pass all "
         "of them to a long-context LLM for synthesis. Costs also "
         "favour RAG: processing 1M tokens per query is expensive."),
        ("Graph RAG",
         "Graph RAG augments retrieval with a knowledge graph built "
         "from the document corpus. Entities and relationships are "
         "extracted by an LLM and stored in a graph database "
         "(Neo4j, NetworkX). Community detection (Leiden algorithm) "
         "groups related entities into communities. Community "
         "summaries are generated by an LLM and stored alongside "
         "raw chunks. Retrieval uses both vector search for chunks "
         "and graph traversal for entity-linked context. Microsoft's "
         "GraphRAG open-source package implements this pipeline. "
         "Graph RAG significantly outperforms naive RAG on queries "
         "requiring synthesis across multiple documents. The tradeoff "
         "is high indexing cost and complexity versus better handling "
         "of global questions about the corpus."),
        ("Agentic RAG",
         "Agentic RAG gives the LLM control over the retrieval "
         "process through tools and reasoning loops. A ReAct agent "
         "alternates between Thought (reasoning), Action (tool call "
         "like search or calculator), and Observation (tool result). "
         "Self-RAG teaches the model to reflect on whether retrieval "
         "is needed and whether retrieved chunks are relevant, using "
         "special tokens. FLARE (Forward-Looking Active Retrieval) "
         "triggers retrieval when the model is about to generate "
         "a low-confidence token. Corrective RAG detects poor "
         "retrieval and falls back to web search. Agentic RAG "
         "handles multi-hop questions naturally but requires more "
         "LLM calls. LangGraph and LlamaIndex agents provide "
         "frameworks for building agentic RAG pipelines."),
        ("Production RAG Best Practices",
         "Deploying RAG in production requires attention to latency, "
         "cost, reliability, and answer quality. Embedding caching "
         "avoids re-embedding unchanged documents. Async retrieval "
         "pipelines reduce end-to-end latency. Rate limiting and "
         "retry logic handle LLM API failures. Prompt templates "
         "should enforce strict instruction following and citation "
         "format. Guardrails check for hallucination, toxicity, and "
         "off-topic responses. Observability tools (LangSmith, "
         "Langfuse, Helicone) log traces for debugging. A/B testing "
         "compares pipeline variants on production traffic. Gradual "
         "rollout with shadow mode validates new retrieval strategies "
         "before full deployment. Data versioning tracks which "
         "document versions are indexed. Regular re-indexing keeps "
         "the knowledge base fresh."),
    ]

    # --- Python & Data Science Tools (10 docs) ---
    tools_docs = [
        ("NumPy for Scientific Computing",
         "NumPy provides the ndarray, a fast multi-dimensional array, "
         "and a comprehensive library of mathematical functions. "
         "Vectorised operations replace Python loops, running in "
         "compiled C code for 10-100x speedup. Broadcasting "
         "automatically aligns arrays of compatible shapes for "
         "element-wise operations. Universal functions (ufuncs) apply "
         "element-wise to arrays with optional output arrays to avoid "
         "allocation. Advanced indexing selects arbitrary array "
         "elements. Linear algebra routines (np.linalg) cover matrix "
         "multiplication, eigendecomposition, SVD, and linear system "
         "solving. Random number generation via np.random.default_rng "
         "supports reproducible seeding. NumPy is the foundation for "
         "SciPy, pandas, scikit-learn, and most of the Python "
         "scientific stack."),
        ("Pandas for Data Manipulation",
         "Pandas provides DataFrame and Series for labelled, "
         "heterogeneous tabular data. Reading data: read_csv(), "
         "read_json(), read_parquet(), read_sql(). Indexing: .loc "
         "for label-based, .iloc for position-based. Groupby applies "
         "split-apply-combine: df.groupby('col').agg(). Merge and "
         "join combine DataFrames on keys or indexes. Reshaping: "
         "pivot_table(), melt(), stack(), unstack(). Time-series "
         "support: DatetimeIndex, resample(), rolling(). Missing "
         "data: fillna(), dropna(), interpolate(). Apply(): row/column "
         "wise function application; map() for Series element-wise. "
         "Categorical dtype reduces memory for low-cardinality "
         "columns. Pandas 2.0 uses PyArrow backend by default for "
         "faster I/O and lower memory."),
        ("Matplotlib and Seaborn Visualisation",
         "Matplotlib is Python's foundational plotting library with "
         "fine-grained control over every visual element. Figure and "
         "Axes objects structure the plot hierarchy. plt.plot() for "
         "line charts; plt.scatter() for scatter plots; plt.bar() "
         "for bar charts; plt.imshow() for heatmaps. Seaborn builds "
         "on Matplotlib with statistical plot types and attractive "
         "themes. sns.histplot() with kde=True shows distributions; "
         "sns.boxplot() and sns.violinplot() compare groups; "
         "sns.heatmap() visualises correlation matrices; sns.pairplot() "
         "gives pairwise scatter plots for exploratory analysis. "
         "Plotly and Bokeh add interactivity. Matplotlib animations "
         "enable visualising dynamic processes."),
        ("Scikit-learn Pipeline",
         "Scikit-learn provides a uniform API: fit(), transform(), "
         "predict() for all estimators. Pipeline chains preprocessing "
         "steps and a final estimator, preventing data leakage and "
         "simplifying cross-validation. ColumnTransformer applies "
         "different transformers to different feature columns. "
         "StandardScaler normalises numerical features; "
         "OneHotEncoder handles categoricals; SimpleImputer fills "
         "missing values. GridSearchCV and RandomizedSearchCV tune "
         "hyperparameters with cross-validation. make_pipeline() "
         "builds pipelines without naming steps. Pipelines are "
         "serialisable with joblib.dump() for deployment. Feature "
         "importance is accessible via .feature_importances_ on "
         "tree-based models or via permutation importance for "
         "model-agnostic analysis."),
        ("LangChain Framework",
         "LangChain is a framework for building LLM applications "
         "using composable components. Chains connect prompts, "
         "models, and output parsers. The LCEL (LangChain Expression "
         "Language) uses the pipe operator (|) to compose chains "
         "declaratively. Retrievers wrap vector stores and provide "
         ".invoke() for document retrieval. RetrievalQA and "
         "ConversationalRetrievalChain build RAG pipelines. Memory "
         "classes (ConversationBufferMemory, ConversationSummaryMemory) "
         "maintain chat history. Agents use tools (search, calculator, "
         "code execution) with ReAct-style reasoning. Callbacks and "
         "LangSmith provide tracing and evaluation. LangChain "
         "integrates with 50+ LLM providers and 100+ vector stores."),
        ("Jupyter Notebooks Best Practices",
         "Jupyter Notebooks combine code, output, and markdown in "
         "an interactive document. Best practices: restart kernel and "
         "run all before committing (ensures top-to-bottom execution). "
         "Use descriptive cell headings in markdown. Keep cells short "
         "and focused; extract reusable code to .py modules. Magic "
         "commands: %timeit for benchmarking, %matplotlib inline for "
         "inline plots, %%writefile to save cell to disk. nbconvert "
         "exports notebooks to HTML, PDF, or slides. JupyterLab "
         "adds file browser, terminal, and extension ecosystem. "
         "nbformat for programmatic notebook creation. "
         "papermill parameterises and executes notebooks from CLI "
         "for pipeline automation. Version control is cleaner with "
         "nbstripout to remove output before committing."),
        ("Docker for ML Projects",
         "Docker containers package ML code, dependencies, and "
         "runtime into reproducible images. A Dockerfile starts "
         "from a base image (python:3.12-slim), copies code, "
         "installs dependencies with pip, and sets an entrypoint. "
         "Multi-stage builds reduce image size by separating build "
         "and runtime environments. Docker Compose orchestrates "
         "multi-container setups (app + database + cache). GPU "
         "support requires NVIDIA Container Toolkit and a "
         "CUDA-enabled base image. .dockerignore excludes data, "
         "checkpoints, and cache from the build context. Volume "
         "mounts persist model checkpoints between runs. "
         "Health checks ensure containers restart on failure. "
         "Container registries (Docker Hub, ECR, GCR) store and "
         "version images for deployment."),
        ("MLflow Experiment Tracking",
         "MLflow tracks machine learning experiments with runs, "
         "parameters, metrics, and artefacts. mlflow.start_run() "
         "opens a run context; log_param(), log_metric(), and "
         "log_artifact() record information. Auto-logging "
         "(mlflow.sklearn.autolog()) captures scikit-learn "
         "model parameters and metrics automatically. The MLflow "
         "UI provides a dashboard for comparing runs and "
         "visualising metric curves. The Model Registry stores "
         "model versions and manages staging, production, and "
         "archived states. MLflow Projects define reproducible "
         "runs via MLproject files with conda or Docker "
         "environments. mlflow.pyfunc wraps any model with a "
         "standard inference interface for deployment to REST "
         "endpoints, SageMaker, or Azure ML."),
        ("Git for ML Projects",
         "Git version-controls code, configuration, and small data "
         "files in ML projects. Branching strategies: main for "
         "stable code, develop for integration, feature/* for new "
         "work. Commit messages should follow Conventional Commits "
         "(feat:, fix:, docs:, refactor:). DVC (Data Version "
         "Control) tracks large files (datasets, model checkpoints) "
         "outside Git using remote storage (S3, GCS, Azure Blob). "
         ".gitignore excludes data/, models/, __pycache__, .env, "
         "*.pyc. Pre-commit hooks run linting (ruff, black, "
         "isort, pycodestyle) before each commit. GitHub Actions "
         "automates CI: install dependencies, run tests, check "
         "code style. Tags mark experiment snapshots for "
         "reproducibility. Git blame and log help trace when "
         "changes to hyperparameters or data processing were "
         "introduced."),
        ("FastAPI for ML Model Serving",
         "FastAPI is a modern Python web framework for building "
         "REST APIs with automatic validation and OpenAPI docs. "
         "Define endpoints with @app.get() / @app.post() decorators "
         "and Pydantic models for request/response schemas. Async "
         "support (async def) enables non-blocking I/O for high "
         "throughput. Model loading on startup via lifespan "
         "context manager avoids per-request overhead. Background "
         "tasks handle long-running inference asynchronously. "
         "Middleware adds CORS, authentication, and rate limiting. "
         "Testing with httpx.AsyncClient and pytest. Uvicorn as "
         "the ASGI server; Gunicorn with Uvicorn workers for "
         "production. Docker + FastAPI is the standard ML serving "
         "stack. Integrates with MLflow model registry for "
         "version-controlled model loading."),
    ]

    # --- AI Ethics & Safety (10 docs) ---
    ethics_docs = [
        ("AI Bias and Fairness",
         "AI systems can perpetuate and amplify societal biases "
         "present in training data. Historical bias (training data "
         "reflects past discrimination), representation bias "
         "(under-represented groups have less data), measurement "
         "bias (proxies introduce error), and aggregation bias "
         "(one model for heterogeneous subgroups). Fairness "
         "metrics: demographic parity (equal positive rate across "
         "groups), equalised odds (equal TPR and FPR), individual "
         "fairness (similar inputs get similar outputs). Mitigation "
         "techniques: pre-processing (resampling, reweighting), "
         "in-processing (fairness constraints in training), "
         "post-processing (threshold adjustment per group). "
         "IBM AI Fairness 360 and Fairlearn are open-source toolkits. "
         "Fairness often involves value-laden tradeoffs between "
         "competing definitions that cannot all be satisfied "
         "simultaneously."),
        ("Explainability and Interpretability",
         "Explainability helps users and regulators understand "
         "AI decisions. Intrinsically interpretable models include "
         "linear regression (coefficients show feature importance), "
         "decision trees (human-readable rules), and GAMs "
         "(generalised additive models). Post-hoc explanation "
         "methods work on any black-box model. LIME (Local "
         "Interpretable Model-agnostic Explanations) fits a simple "
         "model around a prediction. SHAP (SHapley Additive "
         "exPlanations) attributes prediction to features using "
         "Shapley values from cooperative game theory. Integrated "
         "Gradients and GradCAM explain neural network predictions "
         "via gradient attribution. Counterfactual explanations "
         "answer 'what would need to change for a different "
         "outcome'. EU AI Act mandates explanations for high-risk "
         "AI decisions."),
        ("AI Safety and Alignment",
         "AI safety research aims to ensure AI systems behave as "
         "intended without harmful side effects. The alignment "
         "problem: it is hard to specify human values precisely "
         "enough for an AI to optimise them safely. Goodhart's Law "
         "warns that any measure becomes a poor target when optimised "
         "directly. RLHF (RL from Human Feedback) trains models to "
         "match human preferences. Constitutional AI (Anthropic) "
         "uses a set of principles to guide self-improvement. "
         "Scalable oversight proposes methods for humans to evaluate "
         "AI on tasks beyond human ability. Interpretability "
         "research (mechanistic interpretability) aims to understand "
         "what circuits inside neural networks compute. The "
         "Existential risk perspective (Bostrom, Russell) worries "
         "about misaligned superintelligent systems."),
        ("Privacy in AI Systems",
         "AI systems raise significant privacy concerns. Training "
         "data may contain personal information that models "
         "memorise and leak. Membership inference attacks determine "
         "whether a specific record was in the training set. "
         "Model inversion attacks reconstruct training data from "
         "model outputs. Differential privacy adds calibrated noise "
         "during training (DP-SGD) to provide mathematical "
         "guarantees that individual records cannot be inferred. "
         "Federated learning trains models on decentralised devices "
         "without sharing raw data. Synthetic data generation "
         "creates realistic but non-identifying training sets. "
         "GDPR's right to erasure creates challenges for ML: "
         "machine unlearning removes specific data influences "
         "without full retraining. Homomorphic encryption enables "
         "computation on encrypted data."),
        ("Environmental Impact of AI",
         "Training large AI models consumes substantial energy and "
         "produces CO₂ emissions. GPT-3 training was estimated at "
         "552 tCO₂ equivalent. Inference at scale compounds this: "
         "a ChatGPT query uses ~10x the energy of a Google search. "
         "Green AI initiatives focus on efficiency: smaller models, "
         "quantisation, distillation, and sparse architectures "
         "reduce compute. Choosing renewable-energy data centres "
         "lowers carbon footprint. Carbon tracking tools (CodeCarbon, "
         "ML CO2 Impact calculator) estimate emissions per training "
         "run. Hardware efficiency has improved dramatically: H100 "
         "GPUs are 3-4x more energy-efficient than V100. The field "
         "is debating whether AI efficiency gains can offset "
         "the growth in model size and usage."),
        ("Responsible AI Development",
         "Responsible AI integrates ethics into every stage of "
         "the ML lifecycle. Data collection must obtain informed "
         "consent and avoid surveillance or exploitation. Diverse, "
         "representative datasets reduce bias. Model cards "
         "document intended use, limitations, and bias evaluations. "
         "Datasheets for Datasets document provenance, collection "
         "method, and intended use. Red teaming proactively finds "
         "failure modes before deployment. Staged rollout with "
         "monitoring catches harms in production. Feedback "
         "mechanisms allow affected users to report problems. "
         "Governance frameworks (IEEE Ethically Aligned Design, "
         "EU AI Act, NIST AI RMF) provide regulatory guidance. "
         "Multidisciplinary teams including domain experts, "
         "ethicists, and affected communities improve outcomes."),
        ("Hallucination in Language Models",
         "Hallucination refers to LLMs generating plausible-sounding "
         "but factually incorrect content. Intrinsic hallucination "
         "contradicts the input context; extrinsic hallucination "
         "introduces unsupported information. Causes: training on "
         "noisy web data, next-token prediction objective not "
         "grounding truth, knowledge cutoffs. Mitigation: RAG "
         "grounds responses in retrieved documents; self-consistency "
         "sampling checks answer stability; chain-of-thought "
         "prompting improves reasoning. Factuality evaluators "
         "(FActScore, FactBench) benchmark hallucination rates. "
         "RLHF and constitutional AI reduce harmful hallucinations. "
         "Citation generation lets users verify claims. Calibration "
         "research aims to make models express uncertainty when "
         "they do not know an answer."),
        ("Adversarial Attacks on AI",
         "Adversarial attacks add imperceptible perturbations to "
         "inputs that cause AI models to fail. FGSM (Fast Gradient "
         "Sign Method) computes the gradient of the loss with "
         "respect to the input and adds a small step in that "
         "direction. PGD (Projected Gradient Descent) iterates "
         "FGSM while projecting back to an ε-ball. Patch attacks "
         "fool object detectors with visible stickers. Text "
         "adversarial attacks substitute synonyms or add invisible "
         "characters to fool NLP classifiers. Prompt injection "
         "manipulates LLMs via malicious instructions embedded in "
         "user input. Adversarial training (includes adversarial "
         "examples in training) is the most effective defence. "
         "Certified robustness uses randomised smoothing to provide "
         "formal guarantees up to a perturbation radius."),
        ("AI Governance and Regulation",
         "AI governance frameworks aim to ensure AI systems are "
         "safe, fair, and accountable. The EU AI Act (2024) "
         "classifies AI systems by risk: unacceptable (banned), "
         "high-risk (regulated), limited-risk, and minimal-risk. "
         "High-risk applications (biometric ID, credit scoring, "
         "employment screening) require conformity assessments, "
         "human oversight, and transparency. The US AI Executive "
         "Order (Oct 2023) mandates safety evaluations for frontier "
         "models. NIST AI RMF provides a voluntary risk management "
         "framework. GDPR's automated-decision provisions affect "
         "AI-driven decisions with legal effects. China's "
         "generative AI regulations require content moderation "
         "and security assessments. International AI Safety "
         "Institutes coordinate frontier model evaluations."),
        ("Human-AI Collaboration",
         "Human-AI collaboration combines human judgment and "
         "creativity with AI's scale and pattern recognition. "
         "Centaur chess — humans with AI chess engines — "
         "outperforms both alone. Medical AI assists radiologists "
         "with flagging anomalies, reducing miss rates without "
         "replacing clinician judgment. Mixed-initiative systems "
         "let humans and AI dynamically swap control. Human-in-"
         "the-loop ML uses human labellers to correct model "
         "errors and retrain. Active learning queries humans on "
         "the most informative samples. HITL evaluation benchmarks "
         "AI task completion with human oversight. Trust "
         "calibration is critical: over-reliance (automation bias) "
         "and under-reliance both degrade system performance. "
         "UX design for AI tools must make model confidence and "
         "uncertainty visible to users."),
    ]

    topics = [
        ("Machine Learning", ml_docs),
        ("Deep Learning", dl_docs),
        ("NLP", nlp_docs),
        ("Vector Databases", vdb_docs),
        ("RAG", rag_docs),
        ("AI Tools", tools_docs),
        ("AI Ethics", ethics_docs),
    ]

    doc_id = 0
    for topic, docs in topics:
        for i, (title, body) in enumerate(docs, start=1):
            corpus.append((
                f"[{topic}] {title}\n\n{body}",
                f"source_{topic.replace(' ', '_').lower()}",
                f"section_{i:02d}",
                topic,
            ))
            doc_id += 1

    return corpus


# ---------------------------------------------------------------------------
# Chunking (mirrors Day 18/21 approach)
# ---------------------------------------------------------------------------

def chunk_corpus(corpus, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Chunk (text, source, section, topic) tuples using
    RecursiveCharacterTextSplitter and return a list of chunk dicts.
    """
    try:
        from langchain_text_splitters import (  # noqa: PLC0415
            RecursiveCharacterTextSplitter,
        )
    except ImportError:
        from langchain.text_splitter import (  # noqa: PLC0415
            RecursiveCharacterTextSplitter,
        )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    chunks = []
    for i, (text, source, section, topic) in enumerate(corpus):
        for j, chunk in enumerate(splitter.split_text(text)):
            chunks.append({
                "text": chunk,
                "metadata": {
                    "doc_id": i,
                    "chunk_id": j,
                    "source": source,
                    "section": section,
                    "topic": topic,
                },
            })
    return chunks


# ---------------------------------------------------------------------------
# FAISS Document Library
# ---------------------------------------------------------------------------

class DocumentLibrary:
    """FAISS-backed document library with metadata filtering."""

    DIM = 384

    def __init__(self, embedder):
        import faiss  # noqa: PLC0415
        self.embedder = embedder
        self.index = faiss.IndexFlatIP(self.DIM)
        self.chunks = []   # list of chunk dicts in insertion order

    # ------------------------------------------------------------------
    def _normalise(self, vecs):
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        return (vecs / norms).astype(np.float32)

    # ------------------------------------------------------------------
    def build(self, chunks):
        """Embed and index all chunks."""
        texts = [c["text"] for c in chunks]
        raw = np.array(
            self.embedder.embed_documents(texts), dtype=np.float32
        )
        vecs = self._normalise(raw)
        self.index.add(vecs)
        self.chunks = chunks
        print(f"  Indexed {len(chunks)} chunks "
              f"({self.index.ntotal} vectors).")

    # ------------------------------------------------------------------
    def search(self, query, k=5, filter_by=None):
        """
        Search for top-k chunks with optional metadata filtering.

        Parameters
        ----------
        query : str
        k : int
        filter_by : dict | None
            e.g. {"topic": "NLP"} or {"source": "source_nlp"}

        Returns
        -------
        list[dict] with keys: rank, score, text, metadata
        """
        raw = np.array(
            [self.embedder.embed_query(query)], dtype=np.float32
        )
        q_vec = self._normalise(raw)

        # Retrieve larger pool if filtering
        pool_k = min(k * 10, self.index.ntotal) if filter_by else k
        scores, indices = self.index.search(q_vec, pool_k)

        results = []
        rank = 1
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = self.chunks[int(idx)]
            meta = chunk["metadata"]

            # Apply metadata filter
            if filter_by:
                if not all(
                    meta.get(key) == val
                    for key, val in filter_by.items()
                ):
                    continue

            results.append({
                "rank": rank,
                "score": float(score),
                "text": chunk["text"],
                "metadata": meta,
            })
            rank += 1
            if rank > k:
                break

        return results

    # ------------------------------------------------------------------
    def display(self, results, truncate=120):
        """Pretty-print search results."""
        for r in results:
            meta = r["metadata"]
            print(f"\n  #{r['rank']} score={r['score']:.4f} "
                  f"| topic={meta['topic']} "
                  f"| section={meta['section']}")
            print(f"  {r['text'][:truncate]}...")

    # ------------------------------------------------------------------
    def save(self, folder):
        """Persist index + chunks to disk."""
        import faiss  # noqa: PLC0415
        import pickle as pkl  # noqa: PLC0415
        os.makedirs(folder, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder, "lib.faiss"))
        with open(os.path.join(folder, "chunks.pkl"), "wb") as fh:
            pkl.dump(self.chunks, fh)
        print(f"  Library saved to '{folder}/'")


# Alias for the Streamlit dashboard (day22/ui/dashboard.py).
FAISSVectorStore = DocumentLibrary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run Task 2: Document Library with FAISS."""
    output_dir = os.path.join("outputs", "task2")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("Day 22 — Task 2: Document Library with FAISS")
    mode = 'OFFLINE (deterministic)' if USE_OFFLINE else 'ONLINE (MiniLM)'
    print(f'Mode: {mode}')
    print("=" * 60)

    embedder = get_embedder()

    # ------------------------------------------------------------------ #
    # 1. Build corpus & chunk
    # ------------------------------------------------------------------ #
    print("\n[1] Building corpus...")
    corpus = build_corpus()
    print(f"  Documents: {len(corpus)}")

    print("\n[2] Chunking corpus "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    t0 = time.perf_counter()
    chunks = chunk_corpus(corpus)
    chunk_time = time.perf_counter() - t0
    print(f"  Chunks: {len(chunks)} in {chunk_time:.3f}s")

    # ------------------------------------------------------------------ #
    # 2. Build FAISS library
    # ------------------------------------------------------------------ #
    print("\n[3] Embedding & indexing chunks...")
    library = DocumentLibrary(embedder)
    t0 = time.perf_counter()
    library.build(chunks)
    index_time = time.perf_counter() - t0
    print(f"  Indexing time: {index_time:.3f}s")

    # ------------------------------------------------------------------ #
    # 3. Broad search (no filter)
    # ------------------------------------------------------------------ #
    print("\n[4] Search: 'How do transformers handle long sequences?'")
    results = library.search(
        "How do transformers handle long sequences?", k=5
    )
    library.display(results)

    # ------------------------------------------------------------------ #
    # 4. Filtered search — topic = "NLP"
    # ------------------------------------------------------------------ #
    print("\n\n[5] Filtered search (topic=NLP): "
          "'BERT pre-training objectives'")
    results_filtered = library.search(
        "BERT pre-training objectives",
        k=5,
        filter_by={"topic": "NLP"},
    )
    library.display(results_filtered)

    # ------------------------------------------------------------------ #
    # 5. Filtered search — topic = "Vector Databases"
    # ------------------------------------------------------------------ #
    print("\n\n[6] Filtered search (topic=Vector Databases): "
          "'approximate nearest neighbour algorithms'")
    results_vdb = library.search(
        "approximate nearest neighbour algorithms",
        k=5,
        filter_by={"topic": "Vector Databases"},
    )
    library.display(results_vdb)

    # ------------------------------------------------------------------ #
    # 6. Search latency benchmark
    # ------------------------------------------------------------------ #
    print("\n\n[7] Latency benchmark (50 queries)...")
    test_queries = [
        f"question about AI topic number {i}" for i in range(50)
    ]
    t0 = time.perf_counter()
    for q in test_queries:
        library.search(q, k=5)
    elapsed = time.perf_counter() - t0
    avg_ms = (elapsed / 50) * 1000
    print(f"  50 queries in {elapsed:.4f}s  |  avg {avg_ms:.2f} ms/query")

    # ------------------------------------------------------------------ #
    # 7. Save stats JSON
    # ------------------------------------------------------------------ #
    stats = {
        "total_documents": len(corpus),
        "total_chunks": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "indexing_time_s": round(index_time, 4),
        "avg_query_latency_ms": round(avg_ms, 4),
    }
    stats_path = os.path.join(output_dir, "stats.json")
    with open(stats_path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2)
    print(f"\n  Stats written to {stats_path}")

    # ------------------------------------------------------------------ #
    # 8. Persist library
    # ------------------------------------------------------------------ #
    library.save(os.path.join(output_dir, "doc_library"))

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("Task 2 Complete!")
    print(f"  Documents     : {len(corpus)}")
    print(f"  Chunks        : {len(chunks)}")
    print(f"  Chunk size    : {CHUNK_SIZE} chars / {CHUNK_OVERLAP} overlap")
    print(f"  Index time    : {index_time:.3f}s")
    print(f"  Avg latency   : {avg_ms:.2f} ms/query")
    print("=" * 60)


if __name__ == "__main__":
    main()

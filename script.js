let pedido = [];
function criarItemPedido(item) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'pedido-item d-flex justify-content-between align-items-center mb-2';

    // Nome e quantidade
    const descricaoDiv = document.createElement('div');
    descricaoDiv.innerHTML = `
        <strong>${item.nome}</strong>
        <br>
        <small>Quantidade: x${item.quantidade} - R$${item.preco.toFixed(2)} cada</small>
    `;

    // Subtotal
    const subtotalDiv = document.createElement('div');
    subtotalDiv.className = 'text-end text-success fw-bold';
    subtotalDiv.textContent = `R$${(item.quantidade * item.preco).toFixed(2)}`;

    // Adiciona as partes ao item principal
    itemDiv.appendChild(descricaoDiv);
    itemDiv.appendChild(subtotalDiv);

    return itemDiv;
}

// Exemplo: Adicionando os itens no modal
function exibirPedidoModal() {
    const itensPedidoDiv = document.getElementById('itens-pedido'); // Onde os itens serão exibidos
    const taxaEntregaEl = document.getElementById('taxa-entrega');
    const totalPedidoEl = document.getElementById('total-pedido');

    // Limpar itens antigos
    itensPedidoDiv.innerHTML = '';

    let total = 0;
    const taxaEntrega = parseFloat(taxaEntregaEl.textContent.replace('R$', '').trim());

    // Criar itens dinamicamente
    pedido.forEach(item => {
        const itemDiv = criarItemPedido(item);
        itensPedidoDiv.appendChild(itemDiv);
        total += item.quantidade * item.preco;
    });

    // Atualizar o total
    total += taxaEntrega;
    totalPedidoEl.textContent = `R$${total.toFixed(2)}`;
}

function nomeEmpresa() {
    // Capturar a query string da URL
    const params = new URLSearchParams(window.location.search);

    // Obter o valor associado à chave "empresa" (ou qualquer outro parâmetro que você queira capturar)
    const nomeDaEmpresa = params.get('empresa');

    console.log(nomeDaEmpresa); // Exibe o nome da empresa no console
    return nomeDaEmpresa;
}

// Carrega os produtos
async function fetchProdutos() {
    try {
        const response = await fetch(`http://127.0.0.1:5000/precos/empresa/${nomeEmpresa()}`);
        const produtos = await response.json();

        const container = document.getElementById('produtos-container');
        container.innerHTML = '';

        const produtosPorCategoria = {};
        produtos.forEach(produto => {
            const categoria = produto.produto.categoria;
            if (!produtosPorCategoria[categoria]) produtosPorCategoria[categoria] = [];
            produtosPorCategoria[categoria].push(produto);
        });

        const categoriasOrdenadas = Object.keys(produtosPorCategoria).sort();

        const navbarContainer = document.getElementById('navbar-categoria');
        navbarContainer.innerHTML = '';
        categoriasOrdenadas.forEach(categoria => {
            const categoriaLink = document.createElement('a');
            categoriaLink.href = `#categoria-${categoria}`;
            categoriaLink.textContent = categoria;
            categoriaLink.classList.add('nav-item', 'p-1', 'px-md-3');
            categoriaLink.setAttribute('data-categoria', categoria);
            navbarContainer.appendChild(categoriaLink);
        });

        configurarScrollCategorias(categoriasOrdenadas);

        categoriasOrdenadas.forEach(categoria => {
            const categoriaTitulo = document.createElement('h3');
            categoriaTitulo.textContent = categoria;
            categoriaTitulo.classList.add('categoria-titulo', 'mt-4');
            categoriaTitulo.id = `categoria-${categoria}`;
            container.appendChild(categoriaTitulo);

            const categoriaContainer = document.createElement('div');
            categoriaContainer.classList.add('container', 'mb-3');

            const produtosCategoria = produtosPorCategoria[categoria].sort((a, b) => a.produto.nome.localeCompare(b.produto.nome));
            produtosCategoria.forEach(produto => {
                const card = document.createElement('div');
                card.classList.add('card', 'mb-3');
                card.setAttribute('data-id', produto.id);

                card.innerHTML = `
                    <img src="${produto.produto.link_imagem}" alt="Imagem do Produto" class="card-img-top">
                    <div class="card-body">
                        <h5 class="card-title">${produto.produto.nome}</h5>
                        <p class="card-text">${produto.descricao}</p>
                        <p class="price" data-preco="${produto.preco.toFixed(2)}">R$ ${produto.preco.toFixed(2)}</p>
                        <div class="quantity-controls-container">
                            <div class="quantity-controls">
                                <button style="background-color: red;" onclick="alterarQuantidade(${produto.id}, -1)">-</button>
                                <span id="quantidade-${produto.id}" data-id="${produto.id}" data-preco="${produto.preco}">0</span>
                                <button onclick="alterarQuantidade(${produto.id}, 1)">+</button>
                            </div>
                        </div>
                    </div>
                `;
                categoriaContainer.appendChild(card);
            });

            container.appendChild(categoriaContainer);
        });
    } catch (error) {
        console.error('Erro ao carregar os produtos:', error);
    }
}

// Configura a navegação de categorias
function configurarScrollCategorias(categorias) {
    const navbarLinks = document.querySelectorAll('#navbar-categoria a');
    const offsetAdjustment = 60;

    function destacarCategoriaAtiva(categoriaAtiva) {
        navbarLinks.forEach(link => {
            link.classList.toggle('active', link.textContent.trim() === categoriaAtiva);
        });
    }

    let categoriaAtiva = categorias[0];
    destacarCategoriaAtiva(categoriaAtiva);

    window.addEventListener('scroll', () => {
        let categoriaAtivaScroll = null;

        categorias.forEach(categoria => {
            const categoriaElement = document.getElementById(`categoria-${categoria}`);
            if (categoriaElement) {
                const bounding = categoriaElement.getBoundingClientRect();
                if (bounding.top - offsetAdjustment <= window.innerHeight / 2 && bounding.bottom >= offsetAdjustment) {
                    categoriaAtivaScroll = categoria;
                }
            }
        });

        if (!categoriaAtivaScroll) {
            categorias.forEach(categoria => {
                const categoriaElement = document.getElementById(`categoria-${categoria}`);
                if (categoriaElement) {
                    const bounding = categoriaElement.getBoundingClientRect();
                    if (bounding.top <= window.innerHeight && bounding.bottom >= 0) {
                        categoriaAtivaScroll = categoria;
                    }
                }
            });
        }

        if (categoriaAtivaScroll && categoriaAtivaScroll !== categoriaAtiva) {
            categoriaAtiva = categoriaAtivaScroll;
            destacarCategoriaAtiva(categoriaAtiva);
            scrollNavbar(categoriaAtiva);
        }
    });

    document.getElementById('navbar-categoria').addEventListener('click', event => {
        const link = event.target.closest('a');
        if (link) {
            event.preventDefault();
            const targetElement = document.getElementById(`categoria-${link.dataset.categoria}`);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - offsetAdjustment,
                    behavior: 'smooth',
                });
                scrollNavbar(link.dataset.categoria);
            }
        }
    });
}

// Altera a quantidade no cartão
function alterarQuantidade(produtoId, delta) {
    const quantidadeSpan = document.getElementById(`quantidade-${produtoId}`);
    let quantidade = Math.max(0, parseInt(quantidadeSpan.textContent) + delta);
    quantidadeSpan.textContent = quantidade;
    atualizarPedido(produtoId, quantidade);
}
function finalizarPedido(event) {
    event.preventDefault();

    // Coleta os dados dos campos do modal
    const nomeCliente = document.getElementById('nomeCliente').value.trim();
    const endereco = document.getElementById('endereco').value.trim();
    let telefone = document.getElementById('telefone').value.trim();
    
    telefone = telefone.replace(/\D/g, '');

    const metodoPagamento = document.getElementById('metodoPagamento').value;

    // Limpar as mensagens de erro anteriores
    clearErrorMessages();

    let isValid = true;

    // Valida os campos
    if (nomeCliente === "") {
        showError('nomeCliente', "Por favor, insira o seu nome.");
        isValid = false;
    }
    if (endereco === "") {
        showError('endereco', "Por favor, insira o endereço.");
        isValid = false;
    }
    if (!telefone || telefone.length < 10) {
        showError('telefone', "Por favor, insira um telefone válido.");
        isValid = false;
    }
    if (pedido.length === 0) {
        showError('itens-pedido', "Você precisa adicionar pelo menos um item ao pedido.");
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    const listaPrecoProduto = pedido.map(item => item.id);

    // Cria o objeto de dados para enviar ao backend
    const dadosPedido = {
        nome_do_cliente: nomeCliente,
        lista_preco_produto: listaPrecoProduto,
        endereco: endereco,
        contato_cliente: telefone,
        pendente: true
    };

    fetch('http://127.0.0.1:5000/pedidos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dadosPedido)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Pedido finalizado com sucesso', data);

        // Fecha o modal de pedido
        const modalPedido = new bootstrap.Modal(document.getElementById('modalDePedidoLabel'));
        modalPedido.hide();

        // Espera um momento para garantir que o modal de pedido foi fechado antes de abrir o de sucesso
        const modalSucesso = new bootstrap.Modal(document.getElementById('modalSucesso'));
        modalSucesso.show();

        // Limpar os campos após a finalização
        document.getElementById('nomeCliente').value = '';
        document.getElementById('endereco').value = '';
        document.getElementById('telefone').value = '';

        // Limpar as quantidades no DOM
        const quantidadeSpans = document.querySelectorAll('[id^="quantidade-"]');
        quantidadeSpans.forEach(span => span.textContent = '0');

        pedido = []; // Limpa o array de itens do pedido
        atualizarFooter(); // Atualiza o rodapé após o pedido ser limpo
    })
    .catch(error => {
        console.error('Erro ao finalizar o pedido:', error);
        showError('itens-pedido', "Houve um erro ao finalizar o pedido. Tente novamente!");
    });
}


function mascaraTelefone(input) {
    // Remove tudo que não for número
    let valor = input.value.replace(/\D/g, '');

    // Aplica a máscara (formato (XX) XXXXX-XXXX)
    if (valor.length <= 2) {
        input.value = valor.replace(/(\d{2})/, '($1');
    } else if (valor.length <= 6) {
        input.value = valor.replace(/(\d{2})(\d{4})/, '($1) $2');
    } else {
        input.value = valor.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
}

// Função para mostrar mensagens de erro nos inputs
function showError(inputId, message) {
    const inputElement = document.getElementById(inputId);
    const errorMessage = document.createElement('div');
    errorMessage.classList.add('invalid-feedback');
    errorMessage.textContent = message;

    // Adiciona a classe 'is-invalid' ao input
    inputElement.classList.add('is-invalid');

    // Adiciona a mensagem de erro logo abaixo do input
    inputElement.parentElement.appendChild(errorMessage);
}

// Função para limpar mensagens de erro anteriores
function clearErrorMessages() {
    // Remove as classes de erro e as mensagens anteriores
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.classList.remove('is-invalid');
        const errorMessages = input.parentElement.querySelectorAll('.invalid-feedback');
        errorMessages.forEach(msg => msg.remove());
    });
}

// Função para mostrar mensagens de erro nos inputs
function showError(inputId, message) {
    const inputElement = document.getElementById(inputId);
    const errorMessage = document.createElement('div');
    errorMessage.classList.add('invalid-feedback');
    errorMessage.textContent = message;

    // Adiciona a classe 'is-invalid' ao input
    inputElement.classList.add('is-invalid');

    // Adiciona a mensagem de erro logo abaixo do input
    inputElement.parentElement.appendChild(errorMessage);
}

// Função para limpar mensagens de erro anteriores
function clearErrorMessages() {
    // Remove as classes de erro e as mensagens anteriores
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.classList.remove('is-invalid');
        const errorMessages = input.parentElement.querySelectorAll('.invalid-feedback');
        errorMessages.forEach(msg => msg.remove());
    });
}


// Atualiza o pedido
function atualizarPedido(produtoId, quantidade) {
    // Encontra o produto no array de pedidos
    const produto = pedido.find(item => item.id === produtoId);

    if (produto) {
        // Se o produto existir e a quantidade for maior que 0, atualiza a quantidade
        if (quantidade > 0) {
            produto.quantidade = quantidade;
        } else {
            // Se a quantidade for 0, remove o item do pedido
            pedido = pedido.filter(item => item.id !== produtoId);
        }
    } else if (quantidade > 0) {
        // Se o produto não existir no pedido e a quantidade for maior que 0, cria o novo produto
        const produtoNovo = {
            id: produtoId,
            nome: document.querySelector(`#quantidade-${produtoId}`).closest('.card').querySelector('.card-title').textContent,
            preco: parseFloat(document.querySelector(`#quantidade-${produtoId}`).getAttribute('data-preco')),
            quantidade
        };
        pedido.push(produtoNovo);
    }

    // Atualiza o rodapé (total do pedido, etc.)
    atualizarFooter();
}


// Atualiza o footer
function atualizarFooter() {
    const footer = document.querySelector('.footer-fixed');
    const quantidadeItens = pedido.reduce((total, item) => total + item.quantidade, 0);
    const totalPedido = pedido.reduce((total, item) => total + (item.preco * item.quantidade), 0).toFixed(2);

    if (quantidadeItens > 0) {
        footer.style.display = 'block';
        footer.innerHTML = `Finalizar Pedido (${quantidadeItens}) - R$ ${totalPedido}`;
    } else {
        footer.style.display = 'none';
    }
}

// Atualiza o scroll da navbar
function scrollNavbar(categoriaAtiva) {
    const navbarContainer = document.getElementById('navbar-categoria');
    const categoriaLinkAtiva = document.querySelector(`#navbar-categoria a[href="#categoria-${categoriaAtiva}"]`);
    if (categoriaLinkAtiva) {
        navbarContainer.scrollTo({
            left: categoriaLinkAtiva.offsetLeft - navbarContainer.offsetWidth / 2 + categoriaLinkAtiva.offsetWidth / 2,
            behavior: 'smooth',
        });
    }
}

document.addEventListener('DOMContentLoaded', fetchProdutos);
